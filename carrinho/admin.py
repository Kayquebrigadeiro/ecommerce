from django.contrib import admin
from carrinho.models import Carrinho, ItemCarrinho

class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 0
    readonly_fields = ['subtotal']

    def subtotal(self, obj):
        return f"R$ {obj.subtotal():.2f}"
    subtotal.short_description = 'Subtotal'

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'total_itens', 'total', 'data_atualizacao']
    inlines = [ItemCarrinhoInline]
    readonly_fields = ['data_criacao', 'data_atualizacao']

    def total_itens(self, obj):
        return obj.itens.count()
    total_itens.short_description = 'Total de Itens'

    def total(self, obj):
        return f"R$ {obj.calcular_total():.2f}"
    total.short_description = 'Total'

@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ['carrinho', 'produto', 'quantidade', 'subtotal_display', 'data_adicionado']
    list_filter = ['data_adicionado']

    def subtotal_display(self, obj):
        return f"R$ {obj.subtotal():.2f}"
    subtotal_display.short_description = 'Subtotal'
