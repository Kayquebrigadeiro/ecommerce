from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from pagamentos.models import Pagamento
from pedidos.models import Pedido, ItemPedido
from produtos.models import Produto

class PagamentoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.produto = Produto.objects.create(nome='Produto Teste', preco=100.00, estoque=10)
        
        # Criar pedido
        self.pedido = Pedido.objects.create(usuario=self.user, status='pendente')
        ItemPedido.objects.create(
            pedido=self.pedido,
            produto=self.produto,
            quantidade=2,
            preco_unitario=100.00
        )
        self.pedido.recalcular_total()
        
        # Obter token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_criar_pagamento_pix(self):
        response = self.client.post('/api/pagamentos/', {
            'pedido_id': self.pedido.id,
            'metodo': 'pix'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['metodo'], 'pix')
        self.assertEqual(response.data['status'], 'aprovado')  # PIX aprova automaticamente
        self.assertEqual(float(response.data['valor']), 200.0)

    def test_criar_pagamento_cartao(self):
        response = self.client.post('/api/pagamentos/', {
            'pedido_id': self.pedido.id,
            'metodo': 'cartao_credito'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['metodo'], 'cartao_credito')
        self.assertEqual(response.data['status'], 'processando')

    def test_criar_pagamento_pedido_ja_pago(self):
        # Criar primeiro pagamento
        Pagamento.objects.create(
            pedido=self.pedido,
            usuario=self.user,
            metodo='pix',
            valor=self.pedido.total,
            status='aprovado'
        )
        
        # Tentar criar segundo pagamento
        response = self.client.post('/api/pagamentos/', {
            'pedido_id': self.pedido.id,
            'metodo': 'cartao_credito'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_aprovar_pagamento(self):
        pagamento = Pagamento.objects.create(
            pedido=self.pedido,
            usuario=self.user,
            metodo='cartao_credito',
            valor=self.pedido.total,
            status='processando'
        )
        
        response = self.client.post(f'/api/pagamentos/{pagamento.id}/processar/', {
            'acao': 'aprovar',
            'transacao_id': 'TXN123',
            'codigo_autorizacao': 'AUTH456'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pagamento']['status'], 'aprovado')
        
        # Verificar se pedido foi confirmado
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, 'confirmado')

    def test_recusar_pagamento(self):
        pagamento = Pagamento.objects.create(
            pedido=self.pedido,
            usuario=self.user,
            metodo='cartao_credito',
            valor=self.pedido.total,
            status='processando'
        )
        
        response = self.client.post(f'/api/pagamentos/{pagamento.id}/processar/', {
            'acao': 'recusar'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pagamento']['status'], 'recusado')
        
        # Verificar se pedido foi cancelado
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, 'cancelado')

    def test_listar_historico_pagamentos(self):
        # Criar alguns pagamentos
        Pagamento.objects.create(
            pedido=self.pedido,
            usuario=self.user,
            metodo='pix',
            valor=200.00,
            status='aprovado'
        )
        
        response = self.client.get('/api/pagamentos/historico/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
