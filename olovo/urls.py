from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dbolovo.restviews import CollectedSampleViewSet  # Importuj z rest_views.py

router = DefaultRouter()
router.register(r'collected_samples', CollectedSampleViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
]



