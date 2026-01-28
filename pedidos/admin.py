from django.contrib import admin
from pedidos.models import Pedido, ItemPedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'status', 'total', 'data_criacao')
    list_filter = ('status', 'data_criacao')
    search_fields = ('usuario__username', 'id')
    readonly_fields = ('data_criacao', 'data_atualizacao')


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'produto', 'quantidade', 'preco_unitario')
    search_fields = ('pedido__id', 'produto__nome')
