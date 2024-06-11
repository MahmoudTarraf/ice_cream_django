from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import UserProfile
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


from django.contrib.auth.models import User


#login function
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get("username")
        password = request.data.get("password")
        if username and password:
            try:
                user = User.objects.get(username=username)
                if not user.check_password(password):
                    return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
                token, created = Token.objects.get_or_create(user=user)
                user2=UserProfile.objects.get(username=username)
                serializer = UserSerializer(instance=user2)
                return Response({"user": serializer.data})
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
# sign up function
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(username=request.data["username"], password=request.data["password"], email=request.data["email"])

            # Create UserProfile
            phonenumber = request.data.get("phonenumber", "")
            location = request.data.get("location", "")

            UserProfile.objects.create(user=user, username=user.username, email=user.email, phonenumber=phonenumber, location=location)

            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def get_user(request, identifier):
  try:
    user = UserProfile.objects.get(email=identifier)
    serializer = UserSerializer(user)  # Assuming UserSerializer exists
    return Response(serializer.data)
  except UserProfile.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

###

@api_view(['POST'])
def login_admin(request):
    if request.method == 'POST':
        username = request.data.get("username")
        password = request.data.get("password")
        if username and password:
            user = authenticate(request._request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    # login(request._request)  # Use login() from django.contrib.auth
                    return Response({"detail": "Admin login successful."}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Only admins are allowed to login."}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['POST'])
def change_username(request):
    new_username = request.data.get("newUsername")
    username = request.data.get("username")
    email = request.data.get("email")

    if username and email and new_username:
        try:
            if User.objects.filter(username=new_username).exists():
                return Response({"username": "Already Taken!"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(username=username)

            user.username = new_username
            user_profile.username = new_username

            user.save()
            user_profile.save()

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({"detail": "UserProfile not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"detail": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def change_phoneNumber(request):
    phone_number = request.data.get("phonenumber")
    username = request.data.get("username")
    email = request.data.get("email")

    if username and email and phone_number:
        try:
            user_profile = UserProfile.objects.get(email=email)

            if UserProfile.objects.filter(phonenumber=phone_number).exists():
                return Response({"phone_number": "Already Taken!"}, status=status.HTTP_400_BAD_REQUEST)

            user_profile.phonenumber = phone_number
            user_profile.save()

            serializer = UserSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"detail": "UserProfile not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"detail": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def change_email(request):
    new_email = request.data.get("newEmail")
    email = request.data.get("email")
    username = request.data.get("username")

    if username and email and new_email:
        try:
            user = User.objects.get(username=username)

            if user.email == new_email:
                return Response({"email": "Already Exists!"}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=new_email).exists():
                return Response({"email": "Already Taken!"}, status=status.HTTP_400_BAD_REQUEST)

            user_profile = UserProfile.objects.get(username=username)
            user_profile.email = new_email
            user.email=new_email
            user_profile.save()
            user.save()
            serializer = UserSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({"detail": "UserProfile not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"detail": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST)