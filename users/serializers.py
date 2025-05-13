from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=User._meta.get_field('role').choices)

    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'email', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
<<<<<<< HEAD

        fields = ('id', 'full_name', 'phone_number', 'email', 'role')


=======
        fields = ('id', 'full_name', 'phone_number', 'email', 'role')
>>>>>>> b7d6001 (размещение туров)
