from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('cities/<int:city_id>', views.main, name='main'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('accounts/profile/edit', views.profile_edit, name='profile_edit'),
]