from rest_framework import serializers
from pedidos.models import Pedido, ItemPedido


class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    
    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario']


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'usuario_nome', 'data_criacao', 'data_atualizacao', 'status', 'total', 'itens']
        read_only_fields = ['usuario', 'data_criacao', 'data_atualizacao']
