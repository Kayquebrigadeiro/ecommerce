from rest_framework import serializers
from carrinho.models import Carrinho, ItemCarrinho
from produtos.serializers import ProdutoSerializer

class ItemCarrinhoSerializer(serializers.ModelSerializer):
    produto_detalhes = ProdutoSerializer(source='produto', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrinho
        fields = ['id', 'produto', 'produto_detalhes', 'quantidade', 'subtotal', 'data_adicionado']
        read_only_fields = ['data_adicionado']

    def get_subtotal(self, obj):
        return obj.subtotal()

    def validate_quantidade(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantidade deve ser pelo menos 1")
        return value

class CarrinhoSerializer(serializers.ModelSerializer):
    itens = ItemCarrinhoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    total_itens = serializers.SerializerMethodField()

    class Meta:
        model = Carrinho
        fields = ['id', 'usuario', 'itens', 'total', 'total_itens', 'data_criacao', 'data_atualizacao']
        read_only_fields = ['usuario', 'data_criacao', 'data_atualizacao']

    def get_total(self, obj):
        return obj.calcular_total()

    def get_total_itens(self, obj):
        return obj.itens.count()

class AdicionarItemSerializer(serializers.Serializer):
    produto_id = serializers.IntegerField()
    quantidade = serializers.IntegerField(default=1)

    def validate_quantidade(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantidade deve ser pelo menos 1")
        return value

class AtualizarQuantidadeSerializer(serializers.Serializer):
    quantidade = serializers.IntegerField()

    def validate_quantidade(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantidade deve ser pelo menos 1")
        return value
