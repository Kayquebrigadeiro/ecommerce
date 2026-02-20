# 🚀 SportGear Premium - Frontend

E-commerce esportivo premium com design cinematográfico e experiência digital moderna.

## 🎯 Stack Tecnológica

- **Next.js 14** (App Router)
- **TypeScript**
- **TailwindCSS**
- **Framer Motion**
- **Zustand** (Estado Global)
- **React Query** (Data Fetching)
- **Axios** (API Client)

## 🎨 Design System

### Cores
- Background: `#05070D`
- Surface: `#0D111C`
- Primary: `#FF2E2E`
- Secondary: `#00D4FF`
- Text Main: `#E6EDF3`

### Características
- Dark mode premium
- Glassmorphism
- Glow effects
- Gradientes energéticos
- Microinterações
- Animações cinematográficas

## 📦 Instalação

```bash
# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env.local

# Editar .env.local com a URL do backend
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## 🚀 Desenvolvimento

```bash
# Rodar servidor de desenvolvimento
npm run dev

# Abrir http://localhost:3000
```

## 🏗️ Build para Produção

```bash
# Build
npm run build

# Rodar produção localmente
npm start
```

## 📁 Estrutura do Projeto

```
src/
├── app/                    # Páginas Next.js (App Router)
│   ├── page.tsx           # Home
│   ├── produtos/          # Catálogo
│   ├── login/             # Autenticação
│   └── checkout/          # Finalização
├── components/
│   ├── ui/                # Componentes base (Button, Input, Card)
│   ├── layout/            # Navbar, Footer
│   ├── commerce/          # PerformanceCard, CartDrawer
│   ├── motion/            # Componentes animados
│   └── sections/          # Seções da home
├── hooks/                 # Hooks customizados
│   ├── useAuth.ts
│   ├── useCart.ts
│   └── useProducts.ts
├── services/
│   └── api.ts             # Cliente API REST
├── store/
│   └── index.ts           # Zustand stores
├── styles/
│   └── globals.css        # Estilos globais
└── types/
    └── index.ts           # TypeScript types
```

## 🔌 Integração com Backend

O frontend se conecta ao backend Python Django via API REST.

### Endpoints Utilizados

```typescript
// Autenticação
POST /api/token/              // Login
POST /api/register/           // Registro
POST /api/logout/             // Logout

// Produtos
GET /api/produtos/            // Listar produtos
GET /api/produtos/{id}/       // Detalhe do produto

// Carrinho
GET /api/carrinho/            // Ver carrinho
POST /api/carrinho/adicionar/ // Adicionar item
PATCH /api/carrinho/atualizar/{id}/ // Atualizar quantidade
DELETE /api/carrinho/remover/{id}/  // Remover item

// Pedidos
POST /api/pedidos/criar_do_carrinho/ // Criar pedido
GET /api/pedidos/                    // Listar pedidos

// Pagamentos
POST /api/pagamentos/         // Criar pagamento
```

### Autenticação JWT

O frontend armazena tokens JWT no localStorage:

```typescript
localStorage.setItem('access_token', token);
localStorage.setItem('refresh_token', refreshToken);
```

Tokens são automaticamente incluídos nas requisições via interceptor Axios.

## 🎨 Componentes Principais

### UI Base
- `Button` - 4 variantes (primary, ghost, energy, outline)
- `Input` - Input com label e erro
- `Card` - Card com glassmorphism
- `GradientText` - Texto com gradiente

### Motion
- `RevealOnScroll` - Animação ao scroll
- `HoverLiftCard` - Elevação no hover

### Commerce
- `PerformanceCard` - Card de produto premium
- `CartDrawer` - Drawer lateral do carrinho
- `Navbar` - Navegação com scroll effect
- `Footer` - Footer minimalista

### Sections
- `HeroPerformance` - Hero fullscreen cinematográfico
- `FeaturedProductsSection` - Produtos em destaque

## 🎯 Páginas

### Home (`/`)
- Hero cinematográfico
- Produtos em destaque
- Stats animados

### Produtos (`/produtos`)
- Grid de produtos
- Skeleton loading
- Animações no scroll

### Login (`/login`)
- Formulário de login
- Integração com JWT
- Redirecionamento automático

### Checkout (`/checkout`)
- Resumo do pedido
- Seleção de pagamento
- Criação de pedido + pagamento

## 🔧 Hooks Customizados

### `useAuth()`
```typescript
const { user, login, logout, isAuthenticated } = useAuth();
```

### `useCart()`
```typescript
const { cart, addToCart, updateItem, removeItem } = useCart();
```

### `useProducts()`
```typescript
const { data: products, isLoading } = useProducts();
```

## 🎨 Customização

### Cores
Edite `tailwind.config.ts`:

```typescript
colors: {
  background: '#05070D',
  primary: '#FF2E2E',
  // ...
}
```

### Animações
Edite `src/styles/globals.css`:

```css
@keyframes fadeIn {
  /* ... */
}
```

## 📱 Responsividade

O design é totalmente responsivo:
- Mobile: 1 coluna
- Tablet: 2 colunas
- Desktop: 3 colunas

## ⚡ Performance

- Lazy loading de imagens
- Code splitting automático (Next.js)
- React Query cache
- Skeleton loaders

## 🚀 Deploy

### Vercel (Recomendado)

```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel

# Configurar variáveis de ambiente no dashboard
NEXT_PUBLIC_API_URL=https://seu-backend.com
```

### Outras Plataformas

O projeto é compatível com:
- Netlify
- AWS Amplify
- Railway
- Render

## 🔒 Segurança

- Tokens JWT armazenados no localStorage
- Renovação automática de tokens
- Logout em caso de token inválido
- HTTPS obrigatório em produção

## 📝 Variáveis de Ambiente

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_APP_NAME=SportGear Premium
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## 🐛 Troubleshooting

### Erro de CORS
Certifique-se que o backend tem CORS configurado para o domínio do frontend.

### Erro 401 (Unauthorized)
Faça login novamente. O token pode ter expirado.

### Produtos não carregam
Verifique se o backend está rodando e acessível.

## 📚 Documentação Adicional

- [Next.js Docs](https://nextjs.org/docs)
- [TailwindCSS Docs](https://tailwindcss.com/docs)
- [Framer Motion Docs](https://www.framer.com/motion/)
- [React Query Docs](https://tanstack.com/query/latest)

## 🎯 Próximos Passos

- [ ] Adicionar mais páginas (Perfil, Pedidos)
- [ ] Implementar busca de produtos
- [ ] Adicionar filtros por categoria
- [ ] Sistema de wishlist
- [ ] Reviews de produtos
- [ ] Notificações toast
- [ ] PWA support

## 📄 Licença

MIT

---

**Desenvolvido com ⚡ por SportGear Premium**
