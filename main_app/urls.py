from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('accounts/profile/edit', views.profile_edit, name='profile_edit')
]