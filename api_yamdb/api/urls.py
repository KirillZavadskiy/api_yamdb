from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework import routers

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
urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
