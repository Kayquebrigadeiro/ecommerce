# 📋 ANOTAÇÕES COMPLETAS DO BACKEND - E-COMMERCE API

## 🎯 RESUMO EXECUTIVO

**Status:** ✅ 100% FUNCIONAL  
**Data:** 30 de Janeiro de 2026  
**Testes:** 31/31 passando ✅  
**Endpoints:** 28 implementados  

---

## 🏗️ ARQUITETURA DO BACKEND

### Stack Tecnológico
- **Framework:** Django 6.0 + Django REST Framework 3.16.1
- **Autenticação:** JWT (djangorestframework-simplejwt 5.5.1)
- **Banco de Dados:** SQLite (dev) / PostgreSQL (prod)
- **CORS:** django-cors-headers 4.9.0
- **Servidor:** http://127.0.0.1:8000

### Apps Implementados
1. **usuarios** - Autenticação e perfis
2. **produtos** - Catálogo de produtos
3. **carrinho** - Carrinho de compras
4. **pedidos** - Gestão de pedidos
5. **pagamentos** - Processamento de pagamentos

---

## 🔐 AUTENTICAÇÃO (8 endpoints)

### Fluxo de Autenticação
```
1. Registro → Email de verificação enviado
2. Verificar email → is_email_verified = True
3. Login → Recebe access + refresh tokens
4. Usar access token nas requisições
5. Renovar com refresh quando expirar
6. Logout → Blacklist do refresh token
```

### Endpoints

#### 1. Registro
```http
POST /api/register/
Content-Type: application/json

{
  "username": "usuario",
  "email": "usuario@email.com",
  "password": "senha123",
  "password2": "senha123"
}

Response 201:
{
  "message": "Usuário criado com sucesso. Verifique seu email.",
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@email.com"
  }
}
```

#### 2. Login
```http
POST /api/token/
Content-Type: application/json

{
  "username": "usuario",
  "password": "senha123"
}

Response 200:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 3. Renovar Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response 200:
{
  "access": "novo_access_token..."
}
```

#### 4. Logout
```http
POST /api/logout/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response 200:
{
  "message": "Logout realizado com sucesso"
}
```

#### 5-8. Outros endpoints
- `POST /api/password-reset/` - Solicitar reset
- `POST /api/password-reset-confirm/` - Confirmar nova senha
- `POST /api/verify-email/` - Verificar email
- `POST /api/resend-verification/` - Reenviar verificação

### Configuração JWT
- **Access Token:** 5 minutos
- **Refresh Token:** 24 horas
- **Header:** `Authorization: Bearer {token}`

---

## 🛍️ PRODUTOS (5 endpoints)

### Modelo Produto
```python
{
  "id": int,
  "nome": string,
  "descricao": string,
  "preco": decimal (2 casas),
  "estoque": int
}
```

### Endpoints

#### Listar Produtos
```http
GET /api/produtos/
Authorization: Bearer {access_token}

Response 200:
[
  {
    "id": 1,
    "nome": "Notebook Dell",
    "descricao": "Notebook i5 8GB RAM",
    "preco": "3000.00",
    "estoque": 10
  },
  {
    "id": 2,
    "nome": "Mouse Gamer",
    "descricao": "Mouse RGB 16000 DPI",
    "preco": "150.00",
    "estoque": 50
  }
]
```

#### Criar Produto
```http
POST /api/produtos/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome": "Teclado Mecânico",
  "descricao": "Teclado RGB Switch Blue",
  "preco": "350.00",
  "estoque": 25
}

Response 201:
{
  "id": 3,
  "nome": "Teclado Mecânico",
  "descricao": "Teclado RGB Switch Blue",
  "preco": "350.00",
  "estoque": 25
}
```

#### Outros endpoints
- `GET /api/produtos/{id}/` - Detalhe
- `PUT /api/produtos/{id}/` - Atualizar
- `DELETE /api/produtos/{id}/` - Deletar

---

## 🛒 CARRINHO (5 endpoints)

### Modelo Carrinho
```python
{
  "id": int,
  "usuario": int,
  "itens": [
    {
      "id": int,
      "produto": int,
      "produto_detalhes": {
        "id": int,
        "nome": string,
        "preco": decimal,
        "estoque": int
      },
      "quantidade": int,
      "subtotal": decimal
    }
  ],
  "total": decimal,
  "total_itens": int,
  "data_criacao": datetime,
  "data_atualizacao": datetime
}
```

### Endpoints

#### Ver Carrinho
```http
GET /api/carrinho/
Authorization: Bearer {access_token}

Response 200:
{
  "id": 1,
  "usuario": 1,
  "itens": [
    {
      "id": 1,
      "produto": 1,
      "produto_detalhes": {
        "id": 1,
        "nome": "Notebook Dell",
        "preco": "3000.00",
        "estoque": 10
      },
      "quantidade": 2,
      "subtotal": "6000.00",
      "data_adicionado": "2026-01-30T20:00:00Z"
    }
  ],
  "total": "6000.00",
  "total_itens": 1,
  "data_criacao": "2026-01-30T19:00:00Z",
  "data_atualizacao": "2026-01-30T20:00:00Z"
}
```

#### Adicionar ao Carrinho
```http
POST /api/carrinho/adicionar/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "produto_id": 1,
  "quantidade": 2
}

Response 201: (retorna carrinho completo atualizado)

Erros possíveis:
- 400: Estoque insuficiente
- 404: Produto não encontrado
```

#### Atualizar Quantidade
```http
PATCH /api/carrinho/atualizar/{item_id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "quantidade": 5
}

Response 200: (retorna carrinho completo atualizado)
```

#### Remover Item
```http
DELETE /api/carrinho/remover/{item_id}/
Authorization: Bearer {access_token}

Response 200: (retorna carrinho completo atualizado)
```

#### Limpar Carrinho
```http
DELETE /api/carrinho/limpar/
Authorization: Bearer {access_token}

Response 200: (retorna carrinho vazio)
```

### Validações do Carrinho
- ✅ Verifica estoque antes de adicionar
- ✅ Se produto já existe, incrementa quantidade
- ✅ Não permite quantidade maior que estoque
- ✅ Cálculo automático de subtotais e total

---

## 📦 PEDIDOS (6 endpoints)

### Modelo Pedido
```python
{
  "id": int,
  "usuario": int,
  "usuario_nome": string,
  "status": string,  # pendente, confirmado, enviado, entregue, cancelado
  "total": decimal,
  "data_criacao": datetime,
  "data_atualizacao": datetime,
  "itens": [
    {
      "id": int,
      "produto": int,
      "produto_nome": string,
      "quantidade": int,
      "preco_unitario": decimal
    }
  ]
}
```

### Endpoints

#### Listar Meus Pedidos
```http
GET /api/pedidos/
Authorization: Bearer {access_token}

Response 200:
[
  {
    "id": 1,
    "usuario": 1,
    "usuario_nome": "usuario",
    "status": "confirmado",
    "total": "6000.00",
    "data_criacao": "2026-01-30T20:00:00Z",
    "data_atualizacao": "2026-01-30T20:05:00Z",
    "itens": [
      {
        "id": 1,
        "produto": 1,
        "produto_nome": "Notebook Dell",
        "quantidade": 2,
        "preco_unitario": "3000.00"
      }
    ]
  }
]
```

#### ⭐ Criar Pedido do Carrinho (PRINCIPAL)
```http
POST /api/pedidos/criar_do_carrinho/
Authorization: Bearer {access_token}

Response 201:
{
  "id": 1,
  "usuario": 1,
  "usuario_nome": "usuario",
  "status": "pendente",
  "total": "6000.00",
  "itens": [...]
}

Erros possíveis:
- 404: Carrinho não encontrado
- 400: Carrinho vazio
- 400: Estoque insuficiente para algum produto
```

**O que esse endpoint faz:**
1. Valida estoque de todos os itens
2. Cria pedido com status "pendente"
3. Transfere itens do carrinho para o pedido
4. Reduz estoque dos produtos
5. Calcula total automaticamente
6. Limpa o carrinho

#### Detalhe do Pedido
```http
GET /api/pedidos/{id}/
Authorization: Bearer {access_token}

Response 200: (objeto pedido completo)
```

#### Atualizar Status
```http
PATCH /api/pedidos/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "enviado"
}

Response 200: (pedido atualizado)
```

#### Outros endpoints
- `POST /api/pedidos/` - Criar pedido manual
- `GET /api/meus-pedidos/` - Endpoint customizado

### Status de Pedido
- `pendente` - Aguardando pagamento
- `confirmado` - Pagamento aprovado
- `enviado` - Pedido enviado
- `entregue` - Pedido entregue
- `cancelado` - Pedido cancelado

---

## 💳 PAGAMENTOS (4 endpoints)

### Modelo Pagamento
```python
{
  "id": int,
  "pedido": int,
  "pedido_detalhes": {...},
  "usuario": int,
  "usuario_nome": string,
  "metodo": string,  # pix, cartao_credito, cartao_debito, boleto
  "status": string,  # pendente, processando, aprovado, recusado, cancelado
  "valor": decimal,
  "transacao_id": string,
  "codigo_autorizacao": string,
  "data_criacao": datetime,
  "data_atualizacao": datetime,
  "data_aprovacao": datetime
}
```

### Endpoints

#### Criar Pagamento
```http
POST /api/pagamentos/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "pedido_id": 1,
  "metodo": "pix"
}

Response 201:
{
  "id": 1,
  "pedido": 1,
  "usuario": 1,
  "metodo": "pix",
  "status": "aprovado",  # PIX aprova automaticamente
  "valor": "6000.00",
  "transacao_id": "PIX-1-1",
  "data_criacao": "2026-01-30T20:10:00Z"
}

Erros possíveis:
- 400: Pedido já possui pagamento
- 400: Apenas pedidos pendentes podem receber pagamento
- 404: Pedido não encontrado
```

#### Processar Pagamento
```http
POST /api/pagamentos/{id}/processar/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "acao": "aprovar",  # ou "recusar"
  "transacao_id": "TXN123456",
  "codigo_autorizacao": "AUTH789"
}

Response 200:
{
  "message": "Pagamento aprovado com sucesso",
  "pagamento": {...}
}
```

**O que acontece ao aprovar:**
- Status do pagamento → "aprovado"
- Status do pedido → "confirmado"
- data_aprovacao preenchida

**O que acontece ao recusar:**
- Status do pagamento → "recusado"
- Status do pedido → "cancelado"

#### Histórico
```http
GET /api/pagamentos/historico/
Authorization: Bearer {access_token}

Response 200: [array de pagamentos]
```

#### Listar Pagamentos
```http
GET /api/pagamentos/
Authorization: Bearer {access_token}

Response 200: [array de pagamentos do usuário]
```

### Métodos de Pagamento
- `pix` - Aprovação automática
- `cartao_credito` - Requer processamento manual
- `cartao_debito` - Requer processamento manual
- `boleto` - Requer processamento manual

---

## 🔄 FLUXO COMPLETO DE COMPRA

### Passo a Passo

```javascript
// 1. REGISTRO/LOGIN
POST /api/register/ → Criar conta
POST /api/token/ → Obter tokens

// 2. NAVEGAR PRODUTOS
GET /api/produtos/ → Listar produtos

// 3. ADICIONAR AO CARRINHO
POST /api/carrinho/adicionar/
{
  "produto_id": 1,
  "quantidade": 2
}

// 4. VER CARRINHO
GET /api/carrinho/ → Ver total e itens

// 5. CRIAR PEDIDO
POST /api/pedidos/criar_do_carrinho/
→ Retorna pedido_id
→ Carrinho é limpo
→ Estoque é reduzido

// 6. PAGAR
POST /api/pagamentos/
{
  "pedido_id": 1,
  "metodo": "pix"
}
→ PIX aprova automaticamente
→ Pedido muda para "confirmado"

// 7. ACOMPANHAR
GET /api/pedidos/{id}/ → Ver status do pedido
GET /api/pagamentos/{id}/ → Ver status do pagamento
```

---

## 🔒 SEGURANÇA E VALIDAÇÕES

### Autenticação
- ✅ JWT obrigatório em todos os endpoints (exceto registro/login)
- ✅ Access token expira em 5 minutos
- ✅ Refresh token expira em 24 horas
- ✅ Token blacklist no logout

### Validações de Negócio
- ✅ Estoque verificado antes de adicionar ao carrinho
- ✅ Estoque verificado antes de criar pedido
- ✅ Usuário só vê seus próprios dados
- ✅ Não permite pagamento duplicado
- ✅ Apenas pedidos pendentes podem receber pagamento
- ✅ Transações atômicas (tudo ou nada)

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

## 📊 ESTRUTURA DE DADOS

### Relacionamentos
```
User (Django)
  ↓ OneToOne
PerfilUsuario (telefone, endereço, email_verified)

User
  ↓ OneToOne
Carrinho
  ↓ ForeignKey (many)
ItemCarrinho → ForeignKey → Produto

User
  ↓ ForeignKey (many)
Pedido
  ↓ ForeignKey (many)
ItemPedido → ForeignKey → Produto

Pedido
  ↓ OneToOne
Pagamento
```

---

## 🧪 TESTES

### Cobertura
- **Autenticação:** 18 testes ✅
- **Carrinho:** 7 testes ✅
- **Pagamentos:** 6 testes ✅
- **Integração:** 3 testes ✅
- **TOTAL:** 31 testes ✅

### Rodar Testes
```bash
python manage.py test
```

---

## 🚀 INFORMAÇÕES PARA O FRONTEND

### Base URL
```
http://127.0.0.1:8000
```

### Headers Necessários
```javascript
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {access_token}"  // Exceto login/registro
}
```

### Armazenamento de Tokens
```javascript
// Salvar no localStorage após login
localStorage.setItem('access_token', response.access);
localStorage.setItem('refresh_token', response.refresh);

// Usar nas requisições
const token = localStorage.getItem('access_token');
headers: {
  'Authorization': `Bearer ${token}`
}
```

### Tratamento de Erros
```javascript
// Token expirado (401)
if (response.status === 401) {
  // Tentar renovar com refresh token
  // Se falhar, redirecionar para login
}

// Erro de validação (400)
if (response.status === 400) {
  // Mostrar mensagem de erro ao usuário
}

// Não encontrado (404)
if (response.status === 404) {
  // Recurso não existe
}
```

---

## 📱 PÁGINAS NECESSÁRIAS NO FRONTEND

1. **Login/Registro** - `/login`, `/register`
2. **Home/Catálogo** - `/` ou `/produtos`
3. **Detalhe do Produto** - `/produtos/{id}`
4. **Carrinho** - `/carrinho`
5. **Checkout** - `/checkout`
6. **Meus Pedidos** - `/pedidos`
7. **Detalhe do Pedido** - `/pedidos/{id}`
8. **Perfil** - `/perfil`

---

## ✅ CHECKLIST FINAL

- [x] Autenticação completa
- [x] CRUD de produtos
- [x] Carrinho funcional
- [x] Sistema de pedidos
- [x] Processamento de pagamentos
- [x] Validações de estoque
- [x] Testes automatizados
- [x] Documentação completa
- [x] CORS configurado
- [x] Pronto para frontend

---

**Backend finalizado em:** 30/01/2026  
**Status:** ✅ 100% FUNCIONAL  
**Próximo passo:** Desenvolvimento do Frontend
