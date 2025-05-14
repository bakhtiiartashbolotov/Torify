from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        min_length=6
    )
    role = serializers.CharField(read_only=True, default='user')

    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'email', 'password', 'role')
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'required': True},
            'full_name': {'required': True},
            'phone_number': {'required': True},
        }

    def create(self, validated_data):
        user = User(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            role='user',
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ('id', 'full_name', 'phone_number', 'email', 'role')


