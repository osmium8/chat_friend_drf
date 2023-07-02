from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Apps
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('chat.urls')),
    path('api/v1/', include('recommendation.urls')),

    # Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
