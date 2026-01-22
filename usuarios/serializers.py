from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import PerfilUsuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = PerfilUsuario
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        PerfilUsuario.objects.create(user=user)
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer para requisição de reset de senha"""
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Usuário com este email não existe.")
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    """Serializer para confirmar novo password"""
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("As senhas não conferem.")
        return data

class EmailVerificationSerializer(serializers.Serializer):
    """Serializer para verificação de email"""
    token = serializers.CharField()
    
    
class ResendEmailVerificationSerializer(serializers.Serializer):
    """Serializer para reenviar email de verificação"""
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Usuário com este email não existe.")
        return value