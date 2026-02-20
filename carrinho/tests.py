from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from carrinho.models import Carrinho, ItemCarrinho
from produtos.models import Produto

class CarrinhoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.produto1 = Produto.objects.create(nome='Produto 1', preco=100.00, estoque=10)
        self.produto2 = Produto.objects.create(nome='Produto 2', preco=50.00, estoque=5)
        
        # Obter token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_listar_carrinho_vazio(self):
        response = self.client.get('/api/carrinho/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_itens'], 0)
        self.assertEqual(float(response.data['total']), 0.0)

    def test_adicionar_produto_ao_carrinho(self):
        response = self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto1.id,
            'quantidade': 2
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_itens'], 1)
        self.assertEqual(float(response.data['total']), 200.0)

    def test_adicionar_produto_sem_estoque(self):
        response = self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto1.id,
            'quantidade': 20
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Estoque insuficiente', response.data['error'])

    def test_atualizar_quantidade_item(self):
        # Adicionar produto
        self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto1.id,
            'quantidade': 1
        })
        
        carrinho = Carrinho.objects.get(usuario=self.user)
        item = carrinho.itens.first()
        
        # Atualizar quantidade
        response = self.client.patch(f'/api/carrinho/atualizar/{item.id}/', {
            'quantidade': 3
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total']), 300.0)

    def test_remover_item_do_carrinho(self):
        # Adicionar produto
        self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto1.id,
            'quantidade': 1
        })
        
        carrinho = Carrinho.objects.get(usuario=self.user)
        item = carrinho.itens.first()
        
        # Remover item
        response = self.client.delete(f'/api/carrinho/remover/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_itens'], 0)

    def test_limpar_carrinho(self):
        # Adicionar produtos
        self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto1.id,
            'quantidade': 1
        })
        self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto2.id,
            'quantidade': 2
        })
        
        # Limpar carrinho
        response = self.client.delete('/api/carrinho/limpar/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_itens'], 0)

    def test_adicionar_mesmo_produto_incrementa_quantidade(self):
        # Adicionar produto primeira vez
        self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto1.id,
            'quantidade': 2
        })
        
        # Adicionar mesmo produto novamente
        response = self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto1.id,
            'quantidade': 3
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_itens'], 1)
        # 2 + 3 = 5 unidades * 100 = 500
        self.assertEqual(float(response.data['total']), 500.0)
