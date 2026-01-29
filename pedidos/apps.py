from django.apps import AppConfig


class PedidosConfig(AppConfig):
    name = 'pedidos'
    def ready(self):
        #importa singnals para registrar handlers hihi
        import pedidos.signals # noqa: F401

