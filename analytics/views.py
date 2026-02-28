from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class TopRoutesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        mongo_client = getattr(settings, "mongo_client", None)
        if mongo_client is None:
            return Response([])

        pipeline = [
            {"$match": {"endpoint": "/api/trains/search/"}},
            {
                "$group": {
                    "_id": {
                        "src": "$params.source",
                        "dst": "$params.destination",
                    },
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": 5},
        ]

        results = list(mongo_client["irctc"]["api_logs"].aggregate(pipeline))

        data = [
            {
                "source": doc.get("_id", {}).get("src"),
                "destination": doc.get("_id", {}).get("dst"),
                "searches": doc.get("count", 0),
            }
            for doc in results
        ]

        return Response(data)

