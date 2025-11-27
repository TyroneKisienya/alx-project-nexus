from rest_framework import serializers
from django.contrib.auth import get_user_model
from .password_utils import verify_password_reset_token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    model = User
    fields = ['id', 'username', 'email', 'password']
    extra_kwargs = {"email": {"required": True}}
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )
        return user
    
class Userserializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = False, min_length = 6)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            "email": {"required": False},
            "username":{"required": False},
        }

        def update(self, instance, validated_data):
            password = validated_data.pop("password", None)
            instance = super().update(instance, validated_data)
            if password:
                instance.set_password(password)
                instance.save(update_field=['password'])
            return instance
        
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("User does not exist")
        if not user.is_verified:
            raise serializers.ValidationError("Email is not verified")
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confrim_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"passwords": "Not matching"})
        
        user_id, email = verify_password_reset_token(data["token"])
        if not user_id:
            raise serializers.ValidationError({"oken": "Expired or Invalid token"})
        data["user_id"] = user_id
        data["email"] = email
        return data

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "is_active",
            "is_staff",
            "is_verified",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]