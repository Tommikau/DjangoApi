from rest_framework import viewsets, views, status
from .models import Kulutus
from .serialaizers import KulutusSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate, login




@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        print('Received Token in Login:', request.headers.get('Authorization'))

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Get or create a token for the user
            token = Token.objects.get(user=user)

            return Response({'message': 'Login successful', 'token': token.key, 'user_id': user.id, 'username': user.username}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print(f"Login failed: {str(e)}")
        return Response({'error': 'Login failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')  # Plain text password
        email = request.data.get('email')

        # Create the user using create_user method
        user = User.objects.create_user(username=username, password=password, email=email)

        # Generate a token for the user
        token, created = Token.objects.get_or_create(user=user)
        print(f"Token: {token.key}, Created: {created}")
        return Response({'message': 'Registration successful', 'token': token.key}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Registration failed: {str(e)}")
        return Response({'error': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    
class KulutusViewSets(viewsets.ModelViewSet):
    serializer_class = KulutusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Kulutus.objects.filter(user=user)
   
    def perform_create(self, serializer):
        # Lisää automaattisesti kirjautuneen käyttäjän tiedot tallennettavaan tietueeseen
        serializer.save(user=self.request.user)

    
    def create(self, request, *args, **kwargs):
        user_token = request.data.get('user')
        try:
            user_id = User.objects.get(auth_token__key=user_token).id
        except User.DoesNotExist:
            return Response({'error': 'Invalid user token'}, status=status.HTTP_400_BAD_REQUEST)

        # Vaihda 'user' -kenttä 'user_id' -kenttään
        request.data['user'] = user_id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_token = request.data.get('user')

        try:
            user_id = User.objects.get(auth_token__key=user_token).id
        except User.DoesNotExist:
            return Response({'error': 'Invalid user token'}, status=status.HTTP_400_BAD_REQUEST)

        # Vaihda 'user' -kenttä 'user_id' -kenttään
        request.data['user'] = user_id

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)