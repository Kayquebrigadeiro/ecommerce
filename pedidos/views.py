from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from pedidos.models import Pedido, ItemPedido
from pedidos.serializers import PedidoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['post'])
    def criar_do_carrinho(self, request):
        """Cria um pedido a partir do carrinho do usuário"""
        from carrinho.models import Carrinho
        
        try:
            carrinho = Carrinho.objects.get(usuario=request.user)
        except Carrinho.DoesNotExist:
            return Response(
                {"error": "Carrinho não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not carrinho.itens.exists():
            return Response(
                {"error": "Carrinho está vazio"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar estoque de todos os itens
        for item in carrinho.itens.all():
            if item.produto.estoque < item.quantidade:
                return Response(
                    {"error": f"Estoque insuficiente para {item.produto.nome}. Disponível: {item.produto.estoque}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Criar pedido
        with transaction.atomic():
            pedido = Pedido.objects.create(usuario=request.user, status='pendente')
            
            # Transferir itens do carrinho para o pedido
            for item in carrinho.itens.all():
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=item.produto,
                    quantidade=item.quantidade,
                    preco_unitario=item.produto.preco
                )
                # Reduzir estoque
                item.produto.estoque -= item.quantidade
                item.produto.save()
            
            # Calcular total
            pedido.recalcular_total()
            
            # Limpar carrinho
            carrinho.limpar()

        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data)