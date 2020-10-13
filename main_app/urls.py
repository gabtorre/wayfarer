from django.urls import path, include
from . import views
from django.conf.urls.static import static
from wayfare import settings 

from .views import main

urlpatterns = [
    path('', views.home, name='home'),
    path('login_redirect', views.login_redirect, name='login_redirect'),
    path('new_post/<int:city_id>', views.new_post, name='new_post'),
    path('cities/<slug:slug>', main, name='main'),
    path('cities/', views.city, name='city'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('post/<int:post_id>/delete', views.post_delete, name='post_delete'),
    path('profile/<slug:slug>', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('comment/<int:post_id>/', views.post_comment, name='comment')
] +static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)