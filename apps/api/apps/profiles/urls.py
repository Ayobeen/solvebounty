from django.urls import path
from .views import MyProfileView, PublicProfileView

urlpatterns = [
    path('me/profile/', MyProfileView.as_view(), name='my-profile'),
    path('users/<uuid:id>/', PublicProfileView.as_view(), name='public-profile'),
]
