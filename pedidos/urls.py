from django.urls import path
from .views import meus_pedidos

urlpatterns = [
    path("meus pedidos/", meus_pedidos, name="meus_pedidos"),
    
]
