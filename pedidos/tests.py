from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from pedidos.models import Pedido, ItemPedido
from produtos.models import Produto
from decimal import Decimal

class PedidoAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kayquebrigadeiro", password="senha123")
        self.produto = Produto.objects.create(nome="Produto Teste", preco=Decimal('49.90'))
        resp = self.client.post("/api/token/", {"username":"kayquebrigadeiro","password":"senha123"}, format="json")
        self.token = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_listar_pedidos_vazios(self):
        r = self.client.get("/api/meus-pedidos/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, [])
    
    def test_criar_pedido_com_itens_calcula_total(self):
        payload = {
            "status": "pendente",
            "itens": [
                {"produto": self.produto.id, "quantidade": 1, "preco_unitario": str(Decimal('49.90'))},
                {"produto": self.produto.id, "quantidade": 2, "preco_unitario": str(Decimal('49.90'))}
            ]
        } 
        r = self.client.post("/api/pedidos/", payload, format="json")  
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        pedido = Pedido.objects.get(id=r.data['id'])
        self.assertEqual(pedido.total, Decimal('149.70'))
    
    def test_confirmar_sem_itens_rejeita(self):
        payload = {"status": "confirmado"}
        r = self.client.post("/api/pedidos/", payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_atualizar_e_deletar_pedido(self):
        pedido = Pedido.objects.create(usuario=self.user, status="pendente", total=Decimal('0.00'))
        r = self.client.put(f"/api/pedidos/{pedido.id}/", {"status":"confirmado"}, format="json")
        self.assertIn(r.status_code, (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST))
        r = self.client.delete(f"/api/pedidos/{pedido.id}/")
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_quantidade_invalida_rejeita(self):
        """Testa que quantidade < 1 é rejeitada"""
        payload = {
            "status": "pendente",
            "itens": [
                {"produto": self.produto.id, "quantidade": 0, "preco_unitario": str(Decimal('49.90'))}
            ]
        }
        r = self.client.post("/api/pedidos/", payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_produto_inexistente_rejeita(self):
        """Testa que produto inexistente é rejeitado"""
        payload = {
            "status": "pendente",
            "itens": [
                {"produto": 99999, "quantidade": 1, "preco_unitario": str(Decimal('49.90'))}
            ]
        }
        r = self.client.post("/api/pedidos/", payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_usuario_so_ve_proprios_pedidos(self):
        """Testa isolamento de pedidos entre usuários"""
        outro_user = User.objects.create_user(username="outro", password="senha123")
        Pedido.objects.create(usuario=outro_user, status="pendente", total=Decimal('100.00'))
        
        r = self.client.get("/api/pedidos/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)
    
    def test_sem_autenticacao_rejeita(self):
        """Testa que endpoints exigem autenticação"""
        self.client.credentials()
        r = self.client.get("/api/pedidos/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

        
    
    