from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from pedidos.models import Pedido
from.models import Pedido
from pedidos.serializers import PedidoSerializer
# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 🔒 exige login com JWT
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data)