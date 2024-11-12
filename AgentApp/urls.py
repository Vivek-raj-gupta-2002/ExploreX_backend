from django.urls import path
from .views import LatestUserSummaryView

urlpatterns = [
    path('latest_summary/', LatestUserSummaryView.as_view(), name='latest-user-summary'),
]
