from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from carrinho.models import Carrinho, ItemCarrinho
from carrinho.serializers import CarrinhoSerializer, AdicionarItemSerializer, AtualizarQuantidadeSerializer
from produtos.models import Produto

class CarrinhoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Retorna o carrinho do usuário"""
        carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def adicionar(self, request):
        """Adiciona produto ao carrinho"""
        serializer = AdicionarItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        produto_id = serializer.validated_data['produto_id']
        quantidade = serializer.validated_data['quantidade']

        produto = get_object_or_404(Produto, id=produto_id)
        carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)

        # Verificar estoque
        if produto.estoque < quantidade:
            return Response(
                {"error": f"Estoque insuficiente. Disponível: {produto.estoque}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Adicionar ou atualizar item
        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho,
            produto=produto,
            defaults={'quantidade': quantidade}
        )

        if not created:
            item.quantidade += quantidade
            if item.quantidade > produto.estoque:
                return Response(
                    {"error": f"Estoque insuficiente. Disponível: {produto.estoque}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            item.save()

        carrinho_serializer = CarrinhoSerializer(carrinho)
        return Response(carrinho_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch'], url_path='atualizar/(?P<item_id>[^/.]+)')
    def atualizar_quantidade(self, request, item_id=None):
        """Atualiza quantidade de um item"""
        serializer = AtualizarQuantidadeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        carrinho = get_object_or_404(Carrinho, usuario=request.user)
        item = get_object_or_404(ItemCarrinho, id=item_id, carrinho=carrinho)

        nova_quantidade = serializer.validated_data['quantidade']

        if nova_quantidade > item.produto.estoque:
            return Response(
                {"error": f"Estoque insuficiente. Disponível: {item.produto.estoque}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.quantidade = nova_quantidade
        item.save()

        carrinho_serializer = CarrinhoSerializer(carrinho)
        return Response(carrinho_serializer.data)

    @action(detail=False, methods=['delete'], url_path='remover/(?P<item_id>[^/.]+)')
    def remover_item(self, request, item_id=None):
        """Remove item do carrinho"""
        carrinho = get_object_or_404(Carrinho, usuario=request.user)
        item = get_object_or_404(ItemCarrinho, id=item_id, carrinho=carrinho)
        item.delete()

        carrinho_serializer = CarrinhoSerializer(carrinho)
        return Response(carrinho_serializer.data)

    @action(detail=False, methods=['delete'])
    def limpar(self, request):
        """Limpa todo o carrinho"""
        carrinho = get_object_or_404(Carrinho, usuario=request.user)
        carrinho.limpar()

        carrinho_serializer = CarrinhoSerializer(carrinho)
        return Response(carrinho_serializer.data)
