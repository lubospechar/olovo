from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dbolovo.views import MeasureViewSet, LocationViewSet

router = DefaultRouter()
router.register(r"measures", MeasureViewSet, basename="measure")
router.register(r"by-locations", LocationViewSet, basename="location")
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
]



