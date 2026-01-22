# E-Commerce API

## Status do Projeto ✅

**Prioridade Imediata - CONCLUÍDA**

- ✅ **Testes Automatizados** (15 testes passando)
- ✅ **Recuperação de Senha** (endpoints + email)
- ✅ **Verificação de Email** (token + reenvio)
- ✅ **CORS** (configurado e funcional)

**Próximas Etapas**: Segurança em Produção, Docker, Documentação Swagger

---

## Anotações
- Data e horário: 22 de janeiro de 2026
- Projeto Django REST Framework configurado e rodando
- **19:20 - Implementações finalizadas:**
  - ✅ Instalado `djangorestframework-simplejwt` para autenticação JWT
  - ✅ Corrigidos erros de importação em `usuarios/serializers.py` e `views.py` (Perfil → PerfilUsuario)
  - ✅ Corrigido arquivo `ecommerce/urls.py` com imports e rotas corretas
  - ✅ Criado superuser `kayquebrigadeiro`
  - ✅ Token JWT funcionando (access e refresh tokens)
  - ✅ Implementado token blacklist com `rest_framework_simplejwt.token_blacklist`
  - ✅ Criada view de logout (`/api/logout/`) que invalida refresh tokens
  - ✅ Testado com sucesso: obtenção de tokens, renovação e invalidação

- **19:50 - Testes e Recuperação de Senha:**
  - ✅ Implementados 15 testes automatizados (APITestCase) - TODOS PASSANDO
    - Testes de registro, login, refresh de token e logout
    - Testes de fluxo completo de autenticação
  - ✅ Endpoints de recuperação de senha:
    - `POST /api/password-reset/` - Enviar email de reset
    - `POST /api/password-reset-confirm/` - Confirmar nova senha
  - ✅ Validação de token usando PasswordResetTokenGenerator
  - ✅ Configurado backend de email (console para dev)

- **20:10 - Verificação de Email e CORS:**
  - ✅ Adicionados campos `is_email_verified` e `email_verification_token` ao modelo PerfilUsuario
  - ✅ Endpoints de verificação de email:
    - `POST /api/verify-email/` - Verificar email com token
    - `POST /api/resend-verification/` - Reenviar token de verificação
  - ✅ Envio automático de email de verificação no registro
  - ✅ CORS configurado com `django-cors-headers`
    - Permite requisições de `http://localhost:3000` e `http://localhost:8000`
    - Configurado para credenciais (cookies/auth)

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





