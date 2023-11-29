from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework import routers

from api.views import SignUpAPIView, TokenAPIView, UserViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
v1_router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

v1_router.register(
    'users', UserViewSet, basename='users'
)

urlpatterns = [
    path('v1/auth/token/', TokenAPIView.as_view(), name='token'),
    path("v1/", include(v1_router.urls)),
    path('v1/auth/signup/', SignUpAPIView.as_view(), name='signup'),
]
