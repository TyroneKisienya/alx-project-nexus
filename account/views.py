from django.shortcuts import render
from .serializers import RegisterSerializer, Userserializers, ProfileUpdateSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import verify_token, send_verification_email
from .password_utils import validate_password_reset_token, create_password_reset_token

# Create your views here.

User = get_user_model()
class RegisterViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    def create(self, request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_email(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ProfileViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        serializer = Userserializers(request.user, context = {"request": request})
        return Response(serializer.data)
    
    @action(detail=False, methods=["patch"], url_path="me")
    def partial_update_me(self, request):
        serializer = ProfileUpdateSerializer(request.user, data = request.data, partial = True, context = {"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        out = Userserializers(user, context = {"request": request}).data
        return Response(out, status=status.HTTP_200_OK)
    
class LogoutViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"])
    def logout(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout Successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
class EmailVerificationViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"])
    def verify(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"error": "token is required"}, status=400)
        
        user_id, email = verify_token(token)
        if not user_id:
            return Response({"error": "invalid or expired token"}, status=400)
        user = User.objects.filter(id = user_id, email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)
        user.is_verified = True
        user.save()

        return Response({"message": "Email is verified"}, status=200)
    
class PasswordResetViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    # -----------------------------
    # STEP 1: REQUEST RESET EMAIL
    # -----------------------------
    @action(detail=False, methods=["post"], url_path="request")
    def request_reset(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        # generate token
        token = create_password_reset_token(user)

        # send email
        send_verification_email(user, token)

        return Response(
            {"message": "Password reset email sent."},
            status=status.HTTP_200_OK
        )

    # -------------------------------------------------------
    # STEP 2: SUBMIT NEW PASSWORD (AFTER CLICKING RESET LINK)
    # -------------------------------------------------------
    @action(detail=False, methods=["post"], url_path="confirm")
    def confirm_reset(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]
        email = serializer.validated_data["email"]
        new_password = serializer.validated_data["new_password"]

        # get user
        user = User.objects.filter(id=user_id, email=email).first()
        if not user:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # set new password
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )