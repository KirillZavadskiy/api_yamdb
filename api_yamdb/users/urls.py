from django.urls import path


from api.views import (SignUpAPIView, TokenAPIView)

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('token/', TokenAPIView.as_view(), name='get_token'),
]
