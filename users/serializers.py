from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=User._meta.get_field('role').choices)

    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'email', 'role')