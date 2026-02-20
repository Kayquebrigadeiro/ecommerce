from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from pagamentos.models import Pagamento
from pagamentos.serializers import PagamentoSerializer, CriarPagamentoSerializer, ProcessarPagamentoSerializer
from pedidos.models import Pedido

class PagamentoViewSet(viewsets.ModelViewSet):
    serializer_class = PagamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pagamento.objects.filter(usuario=self.request.user)

    def create(self, request):
        """Cria um novo pagamento para um pedido"""
        serializer = CriarPagamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pedido_id = serializer.validated_data['pedido_id']
        metodo = serializer.validated_data['metodo']

        pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)

        # Criar pagamento
        pagamento = Pagamento.objects.create(
            pedido=pedido,
            usuario=request.user,
            metodo=metodo,
            valor=pedido.total,
            status='processando'
        )

        # Simular processamento (em produção, integrar com gateway de pagamento)
        # Por enquanto, aprovar automaticamente PIX e processar outros
        if metodo == 'pix':
            pagamento.transacao_id = f"PIX-{pagamento.id}-{pedido.id}"
            pagamento.aprovar()

        pagamento_serializer = PagamentoSerializer(pagamento)
        return Response(pagamento_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def processar(self, request, pk=None):
        """Processa um pagamento (aprovar/recusar)"""
        pagamento = self.get_object()
        
        if pagamento.status not in ['pendente', 'processando']:
            return Response(
                {"error": "Pagamento já foi processado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProcessarPagamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        acao = serializer.validated_data['acao']
        
        if acao == 'aprovar':
            pagamento.transacao_id = serializer.validated_data.get('transacao_id', f"TXN-{pagamento.id}")
            pagamento.codigo_autorizacao = serializer.validated_data.get('codigo_autorizacao', f"AUTH-{pagamento.id}")
            pagamento.aprovar()
            mensagem = "Pagamento aprovado com sucesso"
        else:
            pagamento.recusar()
            mensagem = "Pagamento recusado"

        pagamento_serializer = PagamentoSerializer(pagamento)
        return Response({
            "message": mensagem,
            "pagamento": pagamento_serializer.data
        })

    @action(detail=False, methods=['get'])
    def historico(self, request):
        """Retorna histórico de pagamentos do usuário"""
        pagamentos = self.get_queryset().order_by('-data_criacao')
        serializer = PagamentoSerializer(pagamentos, many=True)
        return Response(serializer.data)
