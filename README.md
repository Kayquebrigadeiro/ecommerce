# E-Commerce API

## Status do Projeto ✅

**Prioridade Imediata - CONCLUÍDA**

- ✅ **Testes Automatizados** (18 testes passando)
- ✅ **Recuperação de Senha** (endpoints + email + invalidação de tokens)
- ✅ **Verificação de Email** (token com expiração 24h + reenvio)
- ✅ **CORS** (configurado e funcional)
- ✅ **Segurança Avançada** (expiração de tokens, mensagens padronizadas, logout forçado)

**Próximas Etapas**: Segurança em Produção, Docker, Documentação Swagger

---

## 📋 Anotações Completas

### Data: 22 de janeiro de 2026 [15:14]
- **Projeto Django REST Framework configurado e rodando**
- ✅ Instalado `djangorestframework-simplejwt` para autenticação JWT
- ✅ Corrigidos erros de importação em `usuarios/serializers.py` e `views.py` (Perfil → PerfilUsuario)
- ✅ Corrigido arquivo `ecommerce/urls.py` com imports e rotas corretas
- ✅ Criado superuser `kayquebrigadeiro` com senha `senha123`
- ✅ Token JWT funcionando (access e refresh tokens)
- ✅ Implementado token blacklist com `rest_framework_simplejwt.token_blacklist`
- ✅ Criada view de logout (`/api/logout/`) que invalida refresh tokens
- ✅ Testado com sucesso: obtenção de tokens, renovação e invalidação

### Data: 22 de janeiro de 2026 [19:20]
- **Implementações finalizadas - Testes e Recuperação de Senha:**
- ✅ Implementados 15 testes automatizados (APITestCase) - TODOS PASSANDO
  - Testes de registro, login, refresh de token e logout
  - Testes de fluxo completo de autenticação
- ✅ Endpoints de recuperação de senha:
  - `POST /api/password-reset/` - Enviar email de reset
  - `POST /api/password-reset-confirm/` - Confirmar nova senha
- ✅ Validação de token usando PasswordResetTokenGenerator
- ✅ Configurado backend de email (console para dev)

### Data: 22 de janeiro de 2026 [20:10]
- **Verificação de Email e CORS:**
- ✅ Adicionados campos `is_email_verified` e `email_verification_token` ao modelo PerfilUsuario
- ✅ Endpoints de verificação de email:
  - `POST /api/verify-email/` - Verificar email com token
  - `POST /api/resend-verification/` - Reenviar token de verificação
- ✅ Envio automático de email de verificação no registro
- ✅ CORS configurado com `django-cors-headers`
  - Permite requisições de `http://localhost:3000` e `http://localhost:8000`
  - Configurado para credenciais (cookies/auth)

### Data: 23 de janeiro de 2026 [15:33]
- **Melhorias de Segurança e Correções:**
- ✅ **Expiração de Tokens de Verificação de Email (24h)**
  - Adicionado campo `email_verification_expiry: DateTimeField` ao modelo `PerfilUsuario`
  - Tokens de verificação agora expiram em 24 horas a partir da geração
  - `RegisterView` e `ResendEmailVerificationView` atualizada com timestamp de expiração
  - `VerifyEmailView` valida expiração antes de marcar email como verificado
  - Migration criada: `usuarios/migrations/0003_perfilusuario_email_verification_expiry.py`

- ✅ **Mensagens de Resposta Padronizadas**
  - Todas as views agora usam padrão consistente:
    - Sucesso: `{"message": "..."}`
    - Erro: `{"error": "..."}`
  - Aplicado em todas as views de autenticação e verificação

- ✅ **Invalidação de Tokens após Reset de Senha**
  - `SetNewPasswordView` agora invalida todos os refresh tokens ativos do usuário
  - Força logout em todos os dispositivos após reset de senha
  - Utiliza `rest_framework_simplejwt.token_blacklist` para blacklisting de tokens
  - Mensagem atualizada: "Senha resetada com sucesso. Faça login novamente em todos os dispositivos."

- ✅ **Correção de Erros nos Testes**
  - Corrigido typo: `token_urlsafes` → `token_urlsafe`
  - Corrigido uso de `serializer.data` → `serializer.validated_data`
  - Ajustadas URLs dos testes para corresponder às rotas reais
  - **Status Final: 18 testes - TODOS PASSANDO ✅**

### 📊 **Data: 25 de janeiro de 2026 [19:40]** 
#### **RESUMO COMPLETO - PRIORIDADE IMEDIATA CONCLUÍDA**

**🎯 Projeto Base**
- ✅ Django REST Framework 3.14.0 com DRF
- ✅ SQLite3 configurado
- ✅ Apps: usuarios, produtos, pedidos, pagamentos, carrinho
- ✅ Painel Admin Django funcional

**🔐 Autenticação & Segurança**
- ✅ **JWT Token**
  - `djangorestframework-simplejwt` instalado
  - Access token (5min expiração)
  - Refresh token (24h expiração)
  - Token blacklist para logout forçado
  - `POST /api/token/` - Obter tokens
  - `POST /api/token/refresh/` - Renovar access token
  - `POST /api/logout/` - Invalidar tokens (blacklist)

- ✅ **Recuperação de Senha**
  - `POST /api/password-reset/` - Requisita email de reset
  - `POST /api/password-reset-confirm/` - Confirma nova senha
  - Token de reset com expiração de 1 hora
  - Usa `PasswordResetTokenGenerator` do Django
  - **Invalidação automática**: Reset de senha blacklist todos os tokens ativos
  - Força logout em todos os dispositivos após reset

- ✅ **Verificação de Email**
  - `POST /api/verify-email/` - Verifica com token
  - `POST /api/resend-verification/` - Reenvia email
  - Token de verificação com expiração de 24 horas
  - Email automático no registro via `RegisterView`
  - Campo `is_email_verified` no modelo PerfilUsuario
  - Mensagens padronizadas de sucesso/erro

**📧 Email (Backend)**
- ✅ Console backend para desenvolvimento
- ✅ Configurado em `settings.py`
- ✅ Pronto para SMTP em produção (Gmail, etc)

**🌐 CORS**
- ✅ `django-cors-headers` instalado
- ✅ Configurado para:
  - `http://localhost:3000`
  - `http://localhost:8000`
  - `http://127.0.0.1:3000`
  - `http://127.0.0.1:8000`
- ✅ Credenciais ativadas (cookies/auth)

**✅ Testes Automatizados**
- ✅ **18 testes criados com APITestCase**
- ✅ **Status: TODOS PASSANDO 100%**
- ✅ Cobertura:
  - Registro (sucesso, duplicado, sem username)
  - Login (sucesso, senha incorreta, usuário inexistente)
  - Refresh token (sucesso, inválido, faltando)
  - Logout (sucesso, sem auth, sem token, token inválido)
  - Fluxo completo: registro → login → usar → refresh → logout

**📁 Estrutura Implementada**
```
usuarios/
  ├── models.py
  │   └── PerfilUsuario (user, telefone, endereco, is_email_verified, 
  │                      email_verification_token, email_verification_expiry)
  ├── views.py
  │   ├── UserViewSet
  │   ├── PerfilViewSet
  │   ├── RegisterView (com email de verificação)
  │   ├── VerifyEmailView (valida expiração)
  │   ├── ResendEmailVerificationView
  │   ├── logout_view (blacklist refresh token)
  │   ├── PasswordResetRequestView (envia email)
  │   ├── SetNewPasswordView (invalida tokens ativos)
  ├── serializers.py
  │   ├── UserSerializer
  │   ├── PerfilSerializer
  │   ├── RegisterSerializer
  │   ├── EmailVerificationSerializer
  │   ├── ResendEmailVerificationSerializer
  │   ├── PasswordResetRequestSerializer
  │   └── SetNewPasswordSerializer
  ├── tests.py (18 testes com cobertura completa)
  └── migrations/ (3 migrações)

ecommerce/
  ├── settings.py
  │   ├── INSTALLED_APPS (rest_framework, token_blacklist, corsheaders)
  │   ├── MIDDLEWARE (CorsMiddleware adicionado)
  │   ├── CORS_ALLOWED_ORIGINS configurado
  │   ├── EMAIL_BACKEND (console para dev)
  │   └── REST_FRAMEWORK (JWT authentication)
  └── urls.py
      ├── /api/register/
      ├── /api/token/
      ├── /api/token/refresh/
      ├── /api/logout/
      ├── /api/password-reset/
      ├── /api/password-reset-confirm/
      ├── /api/verify-email/
      └── /api/resend-verification/
```

**📦 Dependências Instaladas**
- `django==6.0.1`
- `djangorestframework==3.14.0`
- `djangorestframework-simplejwt==5.3.2`
- `django-cors-headers==4.3.1`
- `python-dotenv` (para variáveis de ambiente)

**⏱️ Tempos de Expiração Configurados**
- Access token: 5 minutos
- Refresh token: 24 horas
- Token de reset de senha: 1 hora
- Token de verificação de email: 24 horas

**🔄 Fluxo de Autenticação Completo**
1. Usuário se registra → Email de verificação enviado
2. Usuário verifica email → `is_email_verified = True`
3. Usuário faz login → Recebe access + refresh tokens
4. Usa access token para requisições protegidas
5. Quando access expirar → Usa refresh para novo access
6. Quando fazer logout → Blacklist do refresh token (logout forçado)
7. Esqueceu senha → Reset com email + novo password + logout forçado

**🎯 Pronto para Produção (Próximos Passos)**
- [ ] ALLOWED_HOSTS, SSL, cookies seguros
- [ ] PostgreSQL em produção
- [ ] Docker + docker-compose
- [ ] Swagger/Redoc para documentação
- [ ] GitHub Actions para CI/CD
- [ ] Rate limiting nos endpoints


## Setup do Projeto

### Criar ambiente virtual
```bash
python -m venv .venv
```

### Ativar ambiente virtual
```bash
.\.venv\Scripts\Activate.ps1
```

### Instalar dependências
```bash
pip install django djangorestframework djangorestframework-simplejwt
```

### Criar migrações e aplicar
```bash
python manage.py makemigrations
python manage.py migrate
```

### Criar superuser
```bash
python manage.py createsuperuser
```

## Rodar o Servidor

```bash
python manage.py runserver
```

O servidor estará disponível em `http://127.0.0.1:8000/`

## Acessar o Painel Admin

1. Acesse: `http://127.0.0.1:8000/admin/`
2. Login com as credenciais do superuser:
   - **Usuário:** kayquebrigadeiro
   - **Senha:** senha123

## Rotas da API

- `http://127.0.0.1:8000/admin/` - Painel Admin
- `http://127.0.0.1:8000/api/` - API
- `http://127.0.0.1:8000/api/register/` - Registro de usuários
- `http://127.0.0.1:8000/api/token/` - Obter token JWT
- `http://127.0.0.1:8000/api/token/refresh/` - Renovar token JWT
- `http://127.0.0.1:8000/api/logout/` - Invalidar refresh token (blacklist)
- `http://127.0.0.1:8000/api/password-reset/` - Requisitar reset de senha
- `http://127.0.0.1:8000/api/password-reset-confirm/` - Confirmar nova senha
- `http://127.0.0.1:8000/api/verify-email/` - Verificar email
- `http://127.0.0.1:8000/api/resend-verification/` - Reenviar verificação de email

## Autenticação JWT

### 1. Obter tokens
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/token/" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username":"kayquebrigadeiro","password":"senha123"}'
```

Resposta:
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

### 2. Renovar access token
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/token/refresh/" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"refresh":"<seu_refresh_token>"}'
```

### 3. Acessar endpoint protegido
```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/api/produtos/" `
  -Headers @{ "Authorization" = "Bearer <access_token>" }
```

### 4. Fazer logout (invalidar token)
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/logout/" `
  -Headers @{ "Authorization" = "Bearer <access_token>"; "Content-Type" = "application/json" } `
  -Body '{"refresh":"<refresh_token>"}'
```

## Recuperação de Senha

### 1. Requisitar reset de senha
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/password-reset/" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"email":"usuario@example.com"}'
```

Resposta:
```json
{
  "message": "Email de reset enviado com sucesso"
}
```

### 2. Confirmar nova senha
Após receber o email, use o token e uidb64:
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/password-reset-confirm/" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"password":"nova_senha_123","password2":"nova_senha_123","uidb64":"<uidb64>","token":"<token>"}'
```

Resposta:
```json
{
  "message": "Senha resetada com sucesso"
}
```

## Testes

### Rodar todos os testes
```bash
python manage.py test usuarios
```

Resultado: **15 testes - TODOS PASSANDO ✅**

### Testes inclusos:
- Registro de usuário
- Login com credenciais
- Refresh de token
- Logout e invalidação de token
- Fluxo completo de autenticação
- Casos de erro (usuário duplicado, credenciais inválidas, etc.)

## Verificação de Email

### 1. Verificar email com token
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/verify-email/" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"token":"<verification_token>"}'
```

### 2. Reenviar token de verificação
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/resend-verification/" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"email":"usuario@example.com"}'
```

## Configuração CORS

A API está configurada para aceitar requisições CORS de:
- `http://localhost:3000` (frontend React/Vue/etc)
- `http://localhost:8000` (frontend local)
- `http://127.0.0.1:3000`
- `http://127.0.0.1:8000`

Para adicionar mais origem, editar `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://seu-dominio.com",
    # ... adicionar mais aqui
]
```

## Estrutura do Projeto

```
ecommerce/
├── ecommerce/          # Configurações do Django
│   ├── settings.py     # Configurações (DB, apps, middleware)
│   ├── urls.py         # Rotas principais
│   ├── wsgi.py
│   └── asgi.py
├── usuarios/           # App de autenticação e usuários
│   ├── models.py       # Modelo PerfilUsuario
│   ├── views.py        # Views de auth, reset de senha, etc
│   ├── serializers.py  # Serializers
│   ├── tests.py        # Testes automatizados
│   └── migrations/
├── produtos/           # App de produtos
├── pedidos/            # App de pedidos
├── pagamentos/         # App de pagamentos
├── carrinho/           # App de carrinho
├── manage.py
└── README.md
```

## Próximos Passos Sugeridos

1. **Segurança em Produção**: Configurar ALLOWED_HOSTS, SSL redirect, cookies seguros
2. **Docker**: Containerizar a aplicação com Docker + docker-compose
3. **Documentação**: Implementar Swagger/Redoc com drf-spectacular
4. **Rate Limiting**: Adicionar throttling do DRF para proteger endpoints
5. **PostgreSQL**: Migrar do SQLite para PostgreSQL
6. **CI/CD**: Configurar GitHub Actions para testes automáticos





