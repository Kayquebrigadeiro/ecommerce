from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.conf import settings
from secrets import token_urlsafe
from .models import PerfilUsuario
from .serializers import (
    UserSerializer, PerfilSerializer, RegisterSerializer,
    PasswordResetRequestSerializer, SetNewPasswordSerializer,
    EmailVerificationSerializer, ResendEmailVerificationSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.all()
    serializer_class = PerfilSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        # Gerar token de verificação
        verification_token = token_urlsafe(32)
        perfil = PerfilUsuario.objects.get(user=user)
        perfil.email_verification_token = verification_token
        perfil.save()
        
        # Enviar email de verificação
        verification_link = f"http://localhost:3000/verify-email/{verification_token}/"
        subject = "Verificação de Email"
        message = f"""
Olá {user.username},

Clique no link abaixo para verificar seu email:
{verification_link}

Este link expira em 24 horas.
"""
        
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_FROM_USER,
                [user.email],
                fail_silently=False
            )
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    View para invalidar o refresh token (blacklist)
    Recebe um POST com o refresh token e o invalida
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response(
            {'message': 'Token foi invalidado com sucesso'},
            status=status.HTTP_205_RESET_CONTENT
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


class VerifyEmailView(generics.GenericAPIView):
    """
    View para verificar email
    Recebe um token de verificação
    """
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            token = serializer.data.get('token')
            perfil = PerfilUsuario.objects.get(email_verification_token=token)
            perfil.is_email_verified = True
            perfil.email_verification_token = ''
            perfil.save()
            
            return Response(
                {'message': 'Email verificado com sucesso'},
                status=status.HTTP_200_OK
            )
        except PerfilUsuario.DoesNotExist:
            return Response(
                {'error': 'Token inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao verificar email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ResendEmailVerificationView(generics.GenericAPIView):
    """
    View para reenviar email de verificação
    """
    serializer_class = ResendEmailVerificationSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            email = serializer.data.get('email')
            user = User.objects.get(email=email)
            perfil = PerfilUsuario.objects.get(user=user)
            
            # Gerar novo token
            verification_token = token_urlsafe(32)
            perfil.email_verification_token = verification_token
            perfil.save()
            
            # Enviar email
            verification_link = f"http://localhost:3000/verify-email/{verification_token}/"
            subject = "Verificação de Email"
            message = f"""
Olá {user.username},

Clique no link abaixo para verificar seu email:
{verification_link}

Este link expira em 24 horas.
"""
            
            send_mail(
                subject,
                message,
                settings.EMAIL_FROM_USER,
                [email],
                fail_silently=False
            )
            
            return Response(
                {'message': 'Email de verificação reenviado com sucesso'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuário não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao reenviar email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PasswordResetRequestView(generics.GenericAPIView):
    """
    View para requisição de reset de senha
    Envia um email com link de reset
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.data.get('email')
        user = User.objects.get(email=email)
        
        # Gerar token e uidb64
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        
        # Construir link de reset
        reset_link = f"http://localhost:3000/password-reset/{uidb64}/{token}/"
        
        # Enviar email
        subject = "Reset de Senha"
        message = f"""
Olá {user.username},

Clique no link abaixo para resetar sua senha:
{reset_link}

Este link expira em 1 hora.
"""
        
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_FROM_USER,
                [email],
                fail_silently=False
            )
            return Response(
                {'message': 'Email de reset enviado com sucesso'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Falha ao enviar email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SetNewPasswordView(generics.GenericAPIView):
    """
    View para confirmar novo password
    Recebe uidb64, token e nova senha
    """
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            password = serializer.data.get('password')
            token = serializer.data.get('token')
            uidb64 = serializer.data.get('uidb64')
            
            # Decodificar user id
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            
            # Verificar token
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Token inválido ou expirado'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Atualizar senha
            user.set_password(password)
            user.save()
            
            return Response(
                {'message': 'Senha resetada com sucesso'},
                status=status.HTTP_200_OK
            )
        
        except DjangoUnicodeDecodeError:
            return Response(
                {'error': 'Token inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuário não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao resetar senha: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )