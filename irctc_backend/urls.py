from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("stations.urls")),
    path("api/", include("trains.urls")),
    path("api/", include("bookings.urls")),
    path("api/analytics/", include("analytics.urls")),
]

