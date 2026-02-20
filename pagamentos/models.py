from django.db import models
from django.contrib.auth.models import User
from pedidos.models import Pedido
from decimal import Decimal

class Pagamento(models.Model):
    METODO_CHOICES = [
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto'),
    ]

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processando', 'Processando'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
        ('cancelado', 'Cancelado'),
        ('estornado', 'Estornado'),
    ]

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='pagamento')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pagamentos')
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Dados do pagamento
    transacao_id = models.CharField(max_length=255, blank=True, null=True)
    codigo_autorizacao = models.CharField(max_length=255, blank=True, null=True)
    
    # Timestamps
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Pagamento #{self.id} - Pedido #{self.pedido.id} ({self.status})"

    def aprovar(self):
        from django.utils import timezone
        self.status = 'aprovado'
        self.data_aprovacao = timezone.now()
        self.save()
        # Atualizar status do pedido
        self.pedido.status = 'confirmado'
        self.pedido.save()

    def recusar(self):
        self.status = 'recusado'
        self.save()
        # Atualizar status do pedido
        self.pedido.status = 'cancelado'
        self.pedido.save()
