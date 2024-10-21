from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, GoodBad, Notes
from .serializers import UserProfileSerializer, GoodBadSerlizer, NotesSerlizer
from django.contrib.auth.models import User  # Assuming you're using Django's User model
from django.utils import timezone

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes_by_date(request, date):
    user = request.user  # Get the current user

    try:
        # Try to fetch the GoodBad object for the user and the given date
        good_bad_entry = Notes.objects.get(user=user, date=date)
        serializer = NotesSerlizer(good_bad_entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except GoodBad.DoesNotExist:
        return Response({"error": "No entry found for the given date."}, status=status.HTTP_404_NOT_FOUND)



# Create or Update a GoodBad object
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_update_notes(request):
    user = request.user  # Get the current user
    data = request.data  # Get the data from the request
    date = timezone.now().date()  # Use today's date

    # Check if a GoodBad object already exists for the user and today's date
    notes_entry, created = Notes.objects.get_or_create(user=user, date=date)

    # print(data, user)
    # Update the GoodBad entry with the new data
    serializer = NotesSerlizer(notes_entry, data=data)
    
    # print(serializer)
    if serializer.is_valid():
        serializer.save()  # Save the updated data
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Create or Update a GoodBad object
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_update_good_bad(request):
    user = request.user  # Get the current user
    data = request.data  # Get the data from the request
    date = timezone.now().date()  # Use today's date

    # Check if a GoodBad object already exists for the user and today's date
    good_bad_entry, created = GoodBad.objects.get_or_create(user=user, date=date)

    # print(data, user)
    # Update the GoodBad entry with the new data
    serializer = GoodBadSerlizer(good_bad_entry, data=data)
    
    # print(serializer)
    if serializer.is_valid():
        serializer.save()  # Save the updated data
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve a GoodBad object by date
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_good_bad_by_date(request, date):
    user = request.user  # Get the current user

    try:
        # Try to fetch the GoodBad object for the user and the given date
        good_bad_entry = GoodBad.objects.get(user=user, date=date)
        serializer = GoodBadSerlizer(good_bad_entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except GoodBad.DoesNotExist:
        return Response({"error": "No entry found for the given date."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    email = request.query_params.get('email')  # Get the email from query parameters
    try:
        user = User.objects.get(email=email)  # Fetch user by email
        user_profile = UserProfile.objects.get(user=user)  # Fetch user profile
        serializer = UserProfileSerializer(user_profile)  # Serialize user profile
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except UserProfile.DoesNotExist:
        return Response({"error": "Profile for this user does not exist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_or_update_profile(request):
    email = request.data.get('email')  # Get the email from the request

    try:
        # print(type(request.data['inputData']))
        # Check if the user already exists
        user = User.objects.get(email=email)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(user_profile, data=request.data['inputData'])

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)