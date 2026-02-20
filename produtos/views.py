from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from produtos.models import Produto
from produtos.serializers import ProdutoSerializer
from pedidos.models import Pedido
from pedidos.serializers import PedidoSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    # permission_classes = [IsAuthenticated]  # Desabilitado para permitir acesso público aos produtos


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 🔒 exige login com JWT
def meus_pedidos(request):
    """Retorna todos os pedidos do usuário autenticado"""
    try:
        # Buscar pedidos do usuário logado
        pedidos = Pedido.objects.filter(usuario=request.user)
        serializer = PedidoSerializer(pedidos, many=True)
        return Response({
            "usuario": request.user.username,
            "total_pedidos": pedidos.count(),
            "pedidos": serializer.data
        })
    except Exception as e:
        return Response({
            "erro": str(e)
        }, status=500)