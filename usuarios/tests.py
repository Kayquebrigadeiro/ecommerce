from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import json


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
