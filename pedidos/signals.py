from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ItemPedido

@receiver(post_save, sender=ItemPedido)
def itempedido_salvo(sender, instance, **kwargs):
    instance.pedido.recalcular_total()

@receiver(post_delete, sender=ItemPedido)
def itempedido_deletado(sender, instance, **kwargs):
    instance.pedido.recalcular_total()