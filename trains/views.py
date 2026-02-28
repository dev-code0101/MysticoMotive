from datetime import datetime
import time

from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Train
from .serializers import TrainSerializer


class TrainAdminView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        """
        Create or update a Train identified by train_number.
        """
        train_number = request.data.get("train_number")
        if not train_number:
            return Response(
                {"train_number": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            instance = Train.objects.get(train_number=train_number)
        except Train.DoesNotExist:
            instance = None

        serializer = TrainSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        train = serializer.save()
        response_status = status.HTTP_200_OK if instance else status.HTTP_201_CREATED
        return Response(TrainSerializer(train).data, status=response_status)


class TrainSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_time = time.time()

        source = request.query_params.get("source")
        destination = request.query_params.get("destination")
        direction = request.query_params.get("direction")

        if not source or not destination:
            return Response(
                {"detail": "source and destination query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        qs = Train.objects.filter(
            route__stations__station__code__iexact=source
        ).filter(
            route__stations__station__code__iexact=destination
        ).distinct()

        if direction:
            normalized = direction.upper()
            qs = qs.filter(direction=normalized)

        # pagination via limit/offset query params
        try:
            limit = int(request.query_params.get("limit", 20))
            offset = int(request.query_params.get("offset", 0))
        except ValueError:
            return Response(
                {"detail": "limit and offset must be integers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sliced_qs = qs[offset : offset + limit]
        serializer = TrainSerializer(sliced_qs, many=True)

        execution_ms = int((time.time() - start_time) * 1000)
        matched_route_ids = list(qs.values_list("route_id", flat=True).distinct())

        log_doc = {
            "endpoint": request.path,
            "method": request.method,
            "params": request.query_params.dict(),
            "user_id": getattr(request.user, "id", None),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "execution_ms": execution_ms,
            "matched_route_ids": matched_route_ids,
        }

        mongo_client = getattr(settings, "mongo_client", None)
        if mongo_client is not None:
            mongo_client["irctc"]["api_logs"].insert_one(log_doc)

        return Response(serializer.data)

