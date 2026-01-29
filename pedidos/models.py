from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Sum
from decimal import Decimal
from produtos.models import Produto

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username} ({self.status})"

    def recalcular_total(self):
        soma = self.itens.aggregate(
            total=Sum(F('quantidade') * F('preco_unitario'))
        )['total'] or Decimal('0.00')
        # Sum retorna Decimal ou None; garantir Decimal com quantize se necessário
        self.total = soma
        self.save(update_fields=['total'])

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        produto_nome = self.produto.nome if self.produto else "Produto removido"
        return f"{self.quantidade}x {produto_nome} (Pedido #{self.pedido.id})"