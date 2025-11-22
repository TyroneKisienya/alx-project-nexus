from rest_framework import serializers
from django.contrib.auth import get_user_model

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