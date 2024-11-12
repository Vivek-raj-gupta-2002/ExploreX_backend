from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserSummary
from .serializers import UserSummarySerializer

class LatestUserSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the latest UserSummary for the authenticated user
        latest_summary = UserSummary.objects.filter(user=request.user).order_by('-date').first()
        
        if latest_summary:
            serializer = UserSummarySerializer(latest_summary)
            return Response(serializer.data, status=200)
        else:
            return Response({"detail": "No summary available"}, status=404)
