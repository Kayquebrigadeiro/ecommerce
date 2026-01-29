from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from pedidos.models import Pedido
from pedidos.serializers import PedidoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data)