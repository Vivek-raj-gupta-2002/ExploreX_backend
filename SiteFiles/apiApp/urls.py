from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    
    path('profiles/', views.get_user_profile, name='get_all_profiles'),
    path('profiles/update/', views.create_or_update_profile, name='create_or_update_profile'),  # New route
    path('goodbad/', views.create_update_good_bad, name='goodbad-create'),
    path('goodbad/<str:date>/', views.get_good_bad_by_date, name='goodbad-detail'),
    path('notes/', views.create_update_notes, name='notes-create'),
    path('notes/<str:date>/', views.get_notes_by_date, name='notes-detail'),
    path('posts/', views.create_post, name='create_post')
]