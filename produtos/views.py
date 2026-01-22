from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from produtos.models import Produto
from produtos.serializers import ProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer