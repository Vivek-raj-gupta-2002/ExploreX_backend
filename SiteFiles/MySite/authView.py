import google.auth.transport.requests
import google.oauth2.id_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class GoogleAuthView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')

        if not token:
            return Response({'error': 'No token provided'}, status=400)

        try:
            # print("pass 1-------->")
            # Set up request object for token verification
            request_adapter = google.auth.transport.requests.Request()
            # print(token)
            # Verify the token against the Google OAuth2 service
            idinfo = google.oauth2.id_token.verify_oauth2_token(
                token,
                request_adapter,
                settings.GOOGLE_CLIENT_ID  # Your web client ID
            )
            # print("pass 2-------->")
            # Log the idinfo to check if verification worked
            # print("Verified token info:", idinfo)

            # Extract user details from the verified token
            

            email = idinfo.get('email')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            picture = idinfo.get('picture')
            
            # Find or create the user in the database
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Return the JWT tokens and user information in the response
            return Response({
                'access': access_token,
                'refresh': str(refresh),
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'profile_pic': picture
                }
            })

        except google.auth.exceptions.GoogleAuthError as e:
            # Handle Google token verification errors
            print("Google token verification failed:", str(e))
            return Response({'error': 'Invalid Google token'}, status=400)
        except ValueError as e:
            # Catch any ValueErrors and print the exception
            print("ValueError during token processing:", str(e))
            return Response({'error': 'Invalid token processing'}, status=400)
