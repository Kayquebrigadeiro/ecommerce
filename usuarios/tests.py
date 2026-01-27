from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import json
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario
from rest_framework import status
from secrets import token_urlsafe
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class RegistroTestCase(APITestCase):
    """Testes para endpoint de registro de usuários"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'
    
    def test_registro_sucesso(self):
        """Teste de registro bem-sucedido"""
        dados = {
            'username': 'novo_usuario',
            'email': 'novo@example.com',
            'password': 'senha_forte_123'
        }
        response = self.client.post(self.register_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
    
    def test_registro_usuario_duplicado(self):
        """Teste de registro com username duplicado"""
        User.objects.create_user(username='existente', email='exist@example.com', password='senha123')
        
        dados = {
            'username': 'existente',
            'email': 'novo@example.com',
            'password': 'senha_forte_123'
        }
        response = self.client.post(self.register_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registro_sem_username(self):
        """Teste de registro sem username"""
        dados = {
            'email': 'novo@example.com',
            'password': 'senha_forte_123'
        }
        response = self.client.post(self.register_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
    """Testes para autenticação JWT (login)"""
    
    def setUp(self):
        self.client = APIClient()
        self.token_url = '/api/token/'
        self.username = 'testuser'
        self.password = 'senha_teste_123'
        self.email = 'test@example.com'
        
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
    
    def test_login_sucesso(self):
        """Teste de login bem-sucedido"""
        dados = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.token_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_senha_incorreta(self):
        """Teste de login com senha incorreta"""
        dados = {
            'username': self.username,
            'password': 'senha_errada'
        }
        response = self.client.post(self.token_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_usuario_inexistente(self):
        """Teste de login com usuário que não existe"""
        dados = {
            'username': 'usuario_inexistente',
            'password': 'qualquer_senha'
        }
        response = self.client.post(self.token_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_sem_credenciais(self):
        """Teste de login sem fornecer username ou password"""
        dados = {}
        response = self.client.post(self.token_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RefreshTokenTestCase(APITestCase):
    """Testes para renovação de token JWT"""
    
    def setUp(self):
        self.client = APIClient()
        self.token_url = '/api/token/'
        self.refresh_url = '/api/token/refresh/'
        self.username = 'testuser'
        self.password = 'senha_teste_123'
        
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        
        # Obter tokens
        response = self.client.post(
            self.token_url,
            {'username': self.username, 'password': self.password},
            format='json'
        )
        self.refresh_token = response.data['refresh']
        self.access_token = response.data['access']
    
    def test_refresh_token_sucesso(self):
        """Teste de renovação de access token bem-sucedida"""
        dados = {'refresh': self.refresh_token}
        response = self.client.post(self.refresh_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        # Access token deve ser diferente
        self.assertNotEqual(response.data['access'], self.access_token)
    
    def test_refresh_token_invalido(self):
        """Teste de renovação com refresh token inválido"""
        dados = {'refresh': 'token_invalido'}
        response = self.client.post(self.refresh_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_refresh_token_faltando(self):
        """Teste de renovação sem fornecer refresh token"""
        dados = {}
        response = self.client.post(self.refresh_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutTestCase(APITestCase):
    """Testes para logout (invalidação de token)"""
    
    def setUp(self):
        self.client = APIClient()
        self.token_url = '/api/token/'
        self.logout_url = '/api/logout/'
        self.username = 'testuser'
        self.password = 'senha_teste_123'
        
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        
        # Obter tokens
        response = self.client.post(
            self.token_url,
            {'username': self.username, 'password': self.password},
            format='json'
        )
        self.refresh_token = response.data['refresh']
        self.access_token = response.data['access']
    
    def test_logout_sucesso(self):
        """Teste de logout bem-sucedido"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        dados = {'refresh': self.refresh_token}
        response = self.client.post(self.logout_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertIn('message', response.data)
    
    def test_logout_sem_autenticacao(self):
        """Teste de logout sem autenticação"""
        dados = {'refresh': self.refresh_token}
        response = self.client.post(self.logout_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_logout_sem_refresh_token(self):
        """Teste de logout sem fornecer refresh token"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        dados = {}
        response = self.client.post(self.logout_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_logout_refresh_token_invalido(self):
        """Teste de logout com refresh token inválido"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        dados = {'refresh': 'token_invalido'}
        response = self.client.post(self.logout_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class IntegracaoFluxoCompletoTestCase(APITestCase):
    """Testes do fluxo completo: registro -> login -> usar -> refresh -> logout"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'
        self.token_url = '/api/token/'
        self.refresh_url = '/api/token/refresh/'
        self.logout_url = '/api/logout/'
        self.produtos_url = '/api/produtos/'
    
    def test_fluxo_completo(self):
        """Teste do fluxo completo de autenticação"""
        # 1. Registro
        dados_registro = {
            'username': 'novo_usuario',
            'email': 'novo@example.com',
            'password': 'senha_forte_123'
        }
        response_registro = self.client.post(self.register_url, dados_registro, format='json')
        self.assertEqual(response_registro.status_code, status.HTTP_201_CREATED)
        
        # 2. Login
        dados_login = {
            'username': 'novo_usuario',
            'password': 'senha_forte_123'
        }
        response_login = self.client.post(self.token_url, dados_login, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        access_token = response_login.data['access']
        refresh_token = response_login.data['refresh']
        
        # 3. Usar endpoint protegido
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response_protegido = self.client.get(self.produtos_url)
        self.assertEqual(response_protegido.status_code, status.HTTP_200_OK)
        
        # 4. Renovar token
        dados_refresh = {'refresh': refresh_token}
        response_refresh = self.client.post(self.refresh_url, dados_refresh, format='json')
        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        novo_access_token = response_refresh.data['access']
        self.assertNotEqual(novo_access_token, access_token)
        
        # 5. Logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {novo_access_token}')
        dados_logout = {'refresh': refresh_token}
        response_logout = self.client.post(self.logout_url, dados_logout, format='json')
        self.assertEqual(response_logout.status_code, status.HTTP_205_RESET_CONTENT)
class EmailVerificationTestCase(APITestCase):
    """Testes para verificação de email"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='senha_forte_123'
        )
        self.perfil = PerfilUsuario.objects.create(user=self.user)
        self.token = token_urlsafe(32)
        self.perfil.email_verification_token = self.token
        self.perfil.save()
        self.verify_url = '/api/verify-email/'
        self.resend_url = '/api/resend-verification/'
    
    def test_verificaçao_email_sucesso(self):
        """Teste de verificação de email bem-sucedida"""
        dados = {'token': self.token}
        response = self.client.post(self.verify_url, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.perfil.refresh_from_db()
        self.assertTrue(self.perfil.is_email_verified)
        
    def test_verificaçao_email_token_invalido(self):
        responce = self.client.post(self.verify_url, {'token': 'token_invalido'}, format='json')
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        self.perfil.refresh_from_db()
        self.assertNotEqual(self.perfil.is_email_verified, True)
class PasswordResetTestCase(APITestCase):
    """Testes para reset de senha"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='senha_forte_123'
        )
        self.reset_request_url = '/api/password-reset/'
        self.reset_confirm_url = '/api/password-reset-confirm/'
    def test_reset_password_flow(self):
        # 1- Solicitar reset de senha, rs gg
        response= self.client.post(self.reset_request_url, {'email': self.user.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 2- Gerar manualmente token e uidb64 hehe
        uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        token = PasswordResetTokenGenerator().make_token(self.user)
        # 3- Confirmar novo password
        dados = {
            "uidb64": uidb64,
            "token": token,
            "password": "novasenha123",
            "password2": "novasenha123"
        }
        response2=self.client.post(self.reset_confirm_url, dados, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        # Recarregar usuário para obter dados atualizados
        self.user.refresh_from_db()
        # Verificar que a senha foi de fato alterada
        self.assertTrue(self.user.check_password('novasenha123'))
        self.assertFalse(self.user.check_password('senha_forte_123'))
        #4- Login com nova senha !!!!!!!!!!
        login = self.client.post('/api/token/', {'username': 'testuser', 'password': 'novasenha123'}, format='json')
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn('access', login.data)