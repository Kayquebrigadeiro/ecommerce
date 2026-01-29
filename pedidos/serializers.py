from rest_framework import serializers
from django.db import transaction
from .models import Pedido, ItemPedido
from produtos.models import Produto
from decimal import Decimal

class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario']

    def validate_quantidade(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantidade deve ser pelo menos 1.")
        return value

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, required=False)
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'usuario_nome', 'data_criacao', 'data_atualizacao', 'status', 'total', 'itens']
        read_only_fields = ['usuario', 'data_criacao', 'data_atualizacao', 'total']

    def validate(self, data):
        status = data.get('status', None)
        itens = self.initial_data.get('itens', None)
        # Se for confirmar no create sem itens, rejeitar
        if status == 'confirmado' and not itens:
            raise serializers.ValidationError("Não é possível confirmar um pedido sem itens.")
        return data

    def create(self, validated_data):
        itens_data = self.initial_data.get('itens', [])
        usuario = self.context['request'].user
        
        with transaction.atomic():
            pedido = Pedido.objects.create(usuario=usuario, status=validated_data.get('status', 'pendente'))
            for item in itens_data:
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto_id=item['produto'],
                    quantidade=item['quantidade'],
                    preco_unitario=Decimal(str(item['preco_unitario']))
                )
            pedido.recalcular_total()
        return pedido

    def update(self, instance, validated_data):
        itens_data = self.initial_data.get('itens', None)
        
        with transaction.atomic():
            instance.status = validated_data.get('status', instance.status)
            instance.save(update_fields=['status'])
            
            if itens_data is not None:
                instance.itens.all().delete()
                for item in itens_data:
                    ItemPedido.objects.create(
                        pedido=instance,
                        produto_id=item['produto'],
                        quantidade=item['quantidade'],
                        preco_unitario=Decimal(str(item['preco_unitario']))
                    )
                instance.recalcular_total()
        return instance