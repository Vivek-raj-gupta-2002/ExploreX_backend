from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.get_user_profile, name='get_all_profiles'),
    path('profiles/update/', views.create_or_update_profile, name='create_or_update_profile'),  # New route
    
]