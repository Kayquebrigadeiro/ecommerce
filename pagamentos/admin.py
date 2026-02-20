from django.contrib import admin
from pagamentos.models import Pagamento

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'usuario', 'metodo', 'status', 'valor', 'data_criacao']
    list_filter = ['status', 'metodo', 'data_criacao']
    search_fields = ['transacao_id', 'codigo_autorizacao', 'usuario__username']
    readonly_fields = ['data_criacao', 'data_atualizacao', 'data_aprovacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('pedido', 'usuario', 'metodo', 'status', 'valor')
        }),
        ('Dados da Transação', {
            'fields': ('transacao_id', 'codigo_autorizacao')
        }),
        ('Timestamps', {
            'fields': ('data_criacao', 'data_atualizacao', 'data_aprovacao')
        }),
    )

    def has_delete_permission(self, request, obj=None):
        # Não permitir deletar pagamentos aprovados
        if obj and obj.status == 'aprovado':
            return False
        return super().has_delete_permission(request, obj)
