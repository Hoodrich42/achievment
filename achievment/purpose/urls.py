from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/<slug:username_slug>/', UserProfile.as_view(), name='profile'),
    path('', Main.as_view(), name='main')
]
