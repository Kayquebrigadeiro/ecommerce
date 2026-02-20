from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from produtos.models import Produto
from carrinho.models import Carrinho
from pedidos.models import Pedido
from pagamentos.models import Pagamento

class FluxoCompletoTestCase(TestCase):
    """Testa o fluxo completo: adicionar ao carrinho → criar pedido → pagar"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='cliente', password='senha123')
        
        # Criar produtos
        self.produto1 = Produto.objects.create(nome='Notebook', preco=3000.00, estoque=5)
        self.produto2 = Produto.objects.create(nome='Mouse', preco=50.00, estoque=20)
        
        # Login
        response = self.client.post('/api/token/', {
            'username': 'cliente',
            'password': 'senha123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_fluxo_completo_compra(self):
        # 1. Adicionar produtos ao carrinho
        response = self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto1.id,
            'quantidade': 1
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto2.id,
            'quantidade': 2
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 2. Verificar carrinho
        response = self.client.get('/api/carrinho/')
        self.assertEqual(response.data['total_itens'], 2)
        self.assertEqual(float(response.data['total']), 3100.0)  # 3000 + (50*2)
        
        # 3. Criar pedido do carrinho
        response = self.client.post('/api/pedidos/criar_do_carrinho/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pedido_id = response.data['id']
        self.assertEqual(float(response.data['total']), 3100.0)
        self.assertEqual(response.data['status'], 'pendente')
        
        # 4. Verificar que carrinho foi limpo
        response = self.client.get('/api/carrinho/')
        self.assertEqual(response.data['total_itens'], 0)
        
        # 5. Verificar que estoque foi reduzido
        self.produto1.refresh_from_db()
        self.produto2.refresh_from_db()
        self.assertEqual(self.produto1.estoque, 4)  # 5 - 1
        self.assertEqual(self.produto2.estoque, 18)  # 20 - 2
        
        # 6. Criar pagamento
        response = self.client.post('/api/pagamentos/', {
            'pedido_id': pedido_id,
            'metodo': 'pix'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'aprovado')
        
        # 7. Verificar que pedido foi confirmado
        response = self.client.get(f'/api/pedidos/{pedido_id}/')
        self.assertEqual(response.data['status'], 'confirmado')

    def test_fluxo_com_estoque_insuficiente(self):
        # Adicionar quantidade maior que estoque
        response = self.client.post('/api/carrinho/adicionar/', {
            'produto_id': self.produto1.id,
            'quantidade': 10  # estoque = 5
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Estoque insuficiente', response.data['error'])

    def test_fluxo_carrinho_vazio(self):
        # Tentar criar pedido com carrinho vazio
        response = self.client.post('/api/pedidos/criar_do_carrinho/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('encontrado', response.data['error'].lower())
