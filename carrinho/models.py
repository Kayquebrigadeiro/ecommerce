from django.db import models
from django.contrib.auth.models import User
from produtos.models import Produto
from decimal import Decimal

class Carrinho(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrinho')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrinho de {self.usuario.username}"

    def calcular_total(self):
        total = sum(item.subtotal() for item in self.itens.all())
        return Decimal(str(total))

    def limpar(self):
        self.itens.all().delete()

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('carrinho', 'produto')

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

    def subtotal(self):
        return self.produto.preco * self.quantidade
