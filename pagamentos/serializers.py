from rest_framework import serializers
from pagamentos.models import Pagamento
from pedidos.serializers import PedidoSerializer

class PagamentoSerializer(serializers.ModelSerializer):
    pedido_detalhes = PedidoSerializer(source='pedido', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Pagamento
        fields = [
            'id', 'pedido', 'pedido_detalhes', 'usuario', 'usuario_nome',
            'metodo', 'status', 'valor', 'transacao_id', 'codigo_autorizacao',
            'data_criacao', 'data_atualizacao', 'data_aprovacao'
        ]
        read_only_fields = ['usuario', 'status', 'data_criacao', 'data_atualizacao', 'data_aprovacao']

    def validate_valor(self, value):
        if value <= 0:
            raise serializers.ValidationError("Valor deve ser maior que zero")
        return value

class CriarPagamentoSerializer(serializers.Serializer):
    pedido_id = serializers.IntegerField()
    metodo = serializers.ChoiceField(choices=Pagamento.METODO_CHOICES)

    def validate_pedido_id(self, value):
        from pedidos.models import Pedido
        try:
            pedido = Pedido.objects.get(id=value)
            if hasattr(pedido, 'pagamento'):
                raise serializers.ValidationError("Este pedido já possui um pagamento")
            if pedido.status != 'pendente':
                raise serializers.ValidationError("Apenas pedidos pendentes podem receber pagamento")
        except Pedido.DoesNotExist:
            raise serializers.ValidationError("Pedido não encontrado")
        return value

class ProcessarPagamentoSerializer(serializers.Serializer):
    acao = serializers.ChoiceField(choices=['aprovar', 'recusar'])
    transacao_id = serializers.CharField(required=False, allow_blank=True)
    codigo_autorizacao = serializers.CharField(required=False, allow_blank=True)
