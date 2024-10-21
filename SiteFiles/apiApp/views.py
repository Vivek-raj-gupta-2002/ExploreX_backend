from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, GoodBad, Notes, Post
from .serializers import UserProfileSerializer, GoodBadSerializer, NotesSerializer, PostSerializer
from django.contrib.auth.models import User
from django.utils import timezone


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    data = request.data  # Get the post data from the request
    serializer = PostSerializer(data=data, context={'user': request.user})  # Pass user in context
    
    if serializer.is_valid():
        serializer.save()  # Save the post with the currently authenticated user
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the created post data with a 201 status

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes_by_date(request, date):
    user = request.user

    try:
        notes_entry = Notes.objects.get(user=user, date=date)
        serializer = NotesSerializer(notes_entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Notes.DoesNotExist:
        return Response({"error": "No entry found for the given date."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_update_notes(request):
    user = request.user
    data = request.data
    date = timezone.now().date()

    notes_entry, created = Notes.objects.get_or_create(user=user, date=date)
    serializer = NotesSerializer(notes_entry, data=data, context={'user': user})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_update_good_bad(request):
    user = request.user
    data = request.data
    date = timezone.now().date()

    good_bad_entry, created = GoodBad.objects.get_or_create(user=user, date=date)
    serializer = GoodBadSerializer(good_bad_entry, data=data, context={'user': user})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_good_bad_by_date(request, date):
    user = request.user

    try:
        good_bad_entry = GoodBad.objects.get(user=user, date=date)
        serializer = GoodBadSerializer(good_bad_entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except GoodBad.DoesNotExist:
        return Response({"error": "No entry found for the given date."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    email = request.query_params.get('email')
    try:
        user = User.objects.get(email=email)
        user_profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except UserProfile.DoesNotExist:
        return Response({"error": "Profile for this user does not exist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_or_update_profile(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(user_profile, data=request.data['inputData'], context={'user': user})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
