from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth.models import User  # Assuming you're using Django's User model

@api_view(['GET'])
def get_user_profile(request):
    email = request.query_params.get('email')  # Get the email from query parameters

    try:
        user = User.objects.get(email=email)  # Fetch user by email
        user_profile = UserProfile.objects.get(user=user)  # Fetch user profile
        serializer = UserProfileSerializer(user_profile)  # Serialize user profile
        
        print(serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except UserProfile.DoesNotExist:
        return Response({"error": "Profile for this user does not exist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_or_update_profile(request):
    email = request.data.get('email')  # Get the email from the request
    # print(email)

    try:
        # Check if the user already exists
        user = User.objects.get(email=email)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
