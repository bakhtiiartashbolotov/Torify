# users/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Поле для ввода пароля (без возвращения в ответе)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    # Поле роли (используем choices из модели)
    role = serializers.ChoiceField(choices=User._meta.get_field('role').choices)

    class Meta:
        model = User
        # Поля, которые клиент может передавать при регистрации
        fields = ('id', 'full_name', 'phone_number', 'email', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Создаём экземпляр User напрямую, без передачи username
        user = User(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        # Устанавливаем пароль (хэшируется внутри модели)
        user.set_password(validated_data['password'])
        # Сохраняем пользователя в БД
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Поля, которые возвращаем клиенту при запросах профиля и т.п.
        fields = ('id', 'full_name', 'phone_number', 'email', 'role')