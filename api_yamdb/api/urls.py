from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import SignUpAPIView, TokenAPIView, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', TokenAPIView.as_view(), name='token'),
    path("v1/", include(router_v1.urls)),
    path('v1/auth/signup/', SignUpAPIView.as_view(), name='signup'),
]
