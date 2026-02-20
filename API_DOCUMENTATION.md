# 📚 DOCUMENTAÇÃO COMPLETA DA API - E-COMMERCE

## 🎯 BACKEND 100% FUNCIONAL ✅

---

## 📊 RESUMO EXECUTIVO

| Módulo | Status | Endpoints | Testes |
|--------|--------|-----------|--------|
| **Autenticação** | ✅ 100% | 8 | 18 ✅ |
| **Produtos** | ✅ 100% | 5 | - |
| **Carrinho** | ✅ 100% | 5 | 7 ✅ |
| **Pedidos** | ✅ 100% | 6 | - |
| **Pagamentos** | ✅ 100% | 4 | 6 ✅ |
| **TOTAL** | ✅ 100% | **28** | **31 ✅** |

---

## 🔐 AUTENTICAÇÃO (8 endpoints)

### 1. Registro de Usuário
```http
POST /api/register/
Content-Type: application/json

{
  "username": "usuario",
  "email": "usuario@email.com",
  "password": "senha123",
  "password2": "senha123"
}
```

**Resposta:**
```json
{
  "message": "Usuário criado com sucesso. Verifique seu email.",
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@email.com"
  }
}
```

### 2. Login (Obter Tokens)
```http
POST /api/token/
Content-Type: application/json

{
  "username": "usuario",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Renovar Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 4. Logout
```http
POST /api/logout/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 5. Solicitar Reset de Senha
```http
POST /api/password-reset/
Content-Type: application/json

{
  "email": "usuario@email.com"
}
```

### 6. Confirmar Nova Senha
```http
POST /api/password-reset-confirm/
Content-Type: application/json

{
  "password": "novaSenha123",
  "password2": "novaSenha123",
  "uidb64": "MQ",
  "token": "abc123..."
}
```

### 7. Verificar Email
```http
POST /api/verify-email/
Content-Type: application/json

{
  "token": "verification_token_here"
}
```

### 8. Reenviar Verificação de Email
```http
POST /api/resend-verification/
Content-Type: application/json

{
  "email": "usuario@email.com"
}
```

---

## 🛍️ PRODUTOS (5 endpoints)

### 1. Listar Produtos
```http
GET /api/produtos/
Authorization: Bearer {access_token}
```

**Resposta:**
```json
[
  {
    "id": 1,
    "nome": "Notebook",
    "descricao": "Notebook Dell i5",
    "preco": "3000.00",
    "estoque": 10
  }
]
```

### 2. Criar Produto
```http
POST /api/produtos/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome": "Mouse Gamer",
  "descricao": "Mouse RGB 16000 DPI",
  "preco": "150.00",
  "estoque": 50
}
```

### 3. Detalhe do Produto
```http
GET /api/produtos/{id}/
Authorization: Bearer {access_token}
```

### 4. Atualizar Produto
```http
PUT /api/produtos/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome": "Mouse Gamer Pro",
  "preco": "180.00",
  "estoque": 45
}
```

### 5. Deletar Produto
```http
DELETE /api/produtos/{id}/
Authorization: Bearer {access_token}
```

---

## 🛒 CARRINHO (5 endpoints)

### 1. Ver Carrinho
```http
GET /api/carrinho/
Authorization: Bearer {access_token}
```

**Resposta:**
```json
{
  "id": 1,
  "usuario": 1,
  "itens": [
    {
      "id": 1,
      "produto": 1,
      "produto_detalhes": {
        "id": 1,
        "nome": "Notebook",
        "preco": "3000.00"
      },
      "quantidade": 2,
      "subtotal": "6000.00"
    }
  ],
  "total": "6000.00",
  "total_itens": 1
}
```

### 2. Adicionar Produto ao Carrinho
```http
POST /api/carrinho/adicionar/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "produto_id": 1,
  "quantidade": 2
}
```

**Validações:**
- ✅ Verifica estoque disponível
- ✅ Se produto já existe, incrementa quantidade
- ✅ Retorna erro se estoque insuficiente

### 3. Atualizar Quantidade
```http
PATCH /api/carrinho/atualizar/{item_id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "quantidade": 5
}
```

### 4. Remover Item
```http
DELETE /api/carrinho/remover/{item_id}/
Authorization: Bearer {access_token}
```

### 5. Limpar Carrinho
```http
DELETE /api/carrinho/limpar/
Authorization: Bearer {access_token}
```

---

## 📦 PEDIDOS (6 endpoints)

### 1. Listar Meus Pedidos
```http
GET /api/pedidos/
Authorization: Bearer {access_token}
```

**Resposta:**
```json
[
  {
    "id": 1,
    "usuario": 1,
    "usuario_nome": "usuario",
    "status": "confirmado",
    "total": "3100.00",
    "data_criacao": "2026-01-30T20:00:00Z",
    "itens": [
      {
        "id": 1,
        "produto": 1,
        "produto_nome": "Notebook",
        "quantidade": 1,
        "preco_unitario": "3000.00"
      }
    ]
  }
]
```

### 2. Criar Pedido do Carrinho ⭐
```http
POST /api/pedidos/criar_do_carrinho/
Authorization: Bearer {access_token}
```

**O que faz:**
- ✅ Valida estoque de todos os itens
- ✅ Cria pedido com status "pendente"
- ✅ Transfere itens do carrinho para o pedido
- ✅ Reduz estoque dos produtos
- ✅ Calcula total automaticamente
- ✅ Limpa o carrinho

**Resposta:**
```json
{
  "id": 1,
  "status": "pendente",
  "total": "3100.00",
  "itens": [...]
}
```

### 3. Criar Pedido Manual
```http
POST /api/pedidos/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "itens": [
    {
      "produto": 1,
      "quantidade": 2,
      "preco_unitario": "3000.00"
    }
  ]
}
```

### 4. Detalhe do Pedido
```http
GET /api/pedidos/{id}/
Authorization: Bearer {access_token}
```

### 5. Atualizar Status do Pedido
```http
PATCH /api/pedidos/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "enviado"
}
```

**Status disponíveis:**
- `pendente`
- `confirmado`
- `enviado`
- `entregue`
- `cancelado`

### 6. Endpoint Customizado - Meus Pedidos
```http
GET /api/meus-pedidos/
Authorization: Bearer {access_token}
```

---

## 💳 PAGAMENTOS (4 endpoints)

### 1. Criar Pagamento
```http
POST /api/pagamentos/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "pedido_id": 1,
  "metodo": "pix"
}
```

**Métodos disponíveis:**
- `cartao_credito`
- `cartao_debito`
- `pix` (aprova automaticamente)
- `boleto`

**Resposta:**
```json
{
  "id": 1,
  "pedido": 1,
  "metodo": "pix",
  "status": "aprovado",
  "valor": "3100.00",
  "transacao_id": "PIX-1-1",
  "data_criacao": "2026-01-30T20:00:00Z"
}
```

### 2. Processar Pagamento (Aprovar/Recusar)
```http
POST /api/pagamentos/{id}/processar/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "acao": "aprovar",
  "transacao_id": "TXN123456",
  "codigo_autorizacao": "AUTH789"
}
```

**Ações:**
- `aprovar` → Muda status para "aprovado" e pedido para "confirmado"
- `recusar` → Muda status para "recusado" e pedido para "cancelado"

### 3. Histórico de Pagamentos
```http
GET /api/pagamentos/historico/
Authorization: Bearer {access_token}
```

### 4. Listar Pagamentos
```http
GET /api/pagamentos/
Authorization: Bearer {access_token}
```

---

## 🔄 FLUXO COMPLETO DE COMPRA

```
1. REGISTRO/LOGIN
   POST /api/register/
   POST /api/token/

2. NAVEGAR PRODUTOS
   GET /api/produtos/

3. ADICIONAR AO CARRINHO
   POST /api/carrinho/adicionar/
   {
     "produto_id": 1,
     "quantidade": 2
   }

4. VER CARRINHO
   GET /api/carrinho/

5. CRIAR PEDIDO DO CARRINHO
   POST /api/pedidos/criar_do_carrinho/
   → Retorna pedido_id

6. CRIAR PAGAMENTO
   POST /api/pagamentos/
   {
     "pedido_id": 1,
     "metodo": "pix"
   }

7. VERIFICAR STATUS
   GET /api/pedidos/{id}/
   GET /api/pagamentos/{id}/
```

---

## 🧪 TESTES

### Rodar Todos os Testes
```bash
python manage.py test
```

### Rodar Testes Específicos
```bash
python manage.py test usuarios      # 18 testes
python manage.py test carrinho      # 7 testes
python manage.py test pagamentos    # 6 testes
python manage.py test core          # 3 testes (integração)
```

### Cobertura de Testes
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

**Total: 31 testes - TODOS PASSANDO ✅**

---

## 🔒 SEGURANÇA

### Autenticação JWT
- Access Token: 5 minutos
- Refresh Token: 24 horas
- Token Blacklist ativado

### Validações
- ✅ Estoque verificado antes de adicionar ao carrinho
- ✅ Estoque verificado antes de criar pedido
- ✅ Usuário só vê seus próprios dados
- ✅ Pagamento só para pedidos pendentes
- ✅ Não permite pagamento duplicado

### CORS
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]
```

---

## 📦 DEPENDÊNCIAS

```txt
django==6.0.1
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.2
django-cors-headers==4.3.1
dj-database-url==3.1.2
whitenoise==6.11.0
python-dotenv
```

---

## 🚀 INICIAR SERVIDOR

```bash
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Aplicar migrações
python manage.py migrate

# Criar superuser (opcional)
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

**Servidor:** http://127.0.0.1:8000/  
**Admin:** http://127.0.0.1:8000/admin/

---

## 📊 ESTRUTURA DO BANCO

### Modelos Implementados

**usuarios**
- User (Django padrão)
- PerfilUsuario (telefone, endereço, verificação de email)

**produtos**
- Produto (nome, descrição, preço, estoque)

**carrinho**
- Carrinho (usuário, timestamps)
- ItemCarrinho (carrinho, produto, quantidade)

**pedidos**
- Pedido (usuário, status, total, timestamps)
- ItemPedido (pedido, produto, quantidade, preço_unitário)

**pagamentos**
- Pagamento (pedido, usuário, método, status, valor, transação_id, timestamps)

---

## ✅ CHECKLIST DE FUNCIONALIDADES

### Autenticação
- [x] Registro de usuários
- [x] Login com JWT
- [x] Refresh de tokens
- [x] Logout com blacklist
- [x] Recuperação de senha
- [x] Verificação de email
- [x] Expiração de tokens

### Produtos
- [x] CRUD completo
- [x] Controle de estoque
- [x] Validações

### Carrinho
- [x] Adicionar produtos
- [x] Atualizar quantidade
- [x] Remover itens
- [x] Limpar carrinho
- [x] Cálculo de total
- [x] Validação de estoque

### Pedidos
- [x] Criar do carrinho
- [x] Criar manual
- [x] Listar pedidos
- [x] Atualizar status
- [x] Cálculo automático de total
- [x] Redução de estoque

### Pagamentos
- [x] Múltiplos métodos
- [x] Aprovação/Recusa
- [x] Histórico
- [x] Integração com pedidos
- [x] Validações

### Testes
- [x] Testes de autenticação (18)
- [x] Testes de carrinho (7)
- [x] Testes de pagamentos (6)
- [x] Testes de integração (3)

---

## 🎯 PRÓXIMOS PASSOS (FRONTEND)

O backend está 100% pronto. Agora você pode criar o frontend com:

1. **Páginas necessárias:**
   - Login/Registro
   - Lista de produtos
   - Detalhe do produto
   - Carrinho
   - Checkout
   - Meus pedidos
   - Perfil do usuário

2. **Tecnologias sugeridas:**
   - HTML5 + CSS3 + JavaScript puro
   - Ou: React/Vue/Angular
   - Fetch API para chamadas HTTP
   - LocalStorage para tokens

3. **Design System:**
   - Cores, tipografia, componentes
   - Responsivo (mobile-first)
   - UX otimizada

---

**Backend finalizado em:** 30/01/2026  
**Status:** ✅ 100% FUNCIONAL  
**Pronto para:** Frontend Development
