from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from produtos.views import ProdutoViewSet, meus_pedidos
from usuarios.views import (
    UserViewSet, PerfilViewSet, RegisterView, logout_view,
    PasswordResetRequestView, SetNewPasswordView,
    VerifyEmailView, ResendEmailVerificationView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'perfis', PerfilViewSet)
router.register(r'produtos', ProdutoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', logout_view, name='logout'),
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/password-reset-confirm/', SetNewPasswordView.as_view(), name='password_reset_confirm'),
    path('api/verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('api/resend-verification/', ResendEmailVerificationView.as_view(), name='resend_verification'),
    path('api/meus-pedidos/', meus_pedidos, name='meus_pedidos'),
]
