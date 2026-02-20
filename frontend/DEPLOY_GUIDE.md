# 🚀 GUIA COMPLETO DE DEPLOY - SPORTGEAR PREMIUM

## 📋 VISÃO GERAL

Este guia cobre o deploy completo do projeto:
- **Frontend**: Next.js → Vercel
- **Backend**: Django → Railway/Render
- **Banco de Dados**: PostgreSQL

---

## 🎯 PARTE 1: DEPLOY DO BACKEND (Django)

### Opção A: Railway (Recomendado)

#### 1. Preparar o Backend

```bash
cd c:\ecommerce

# Criar requirements.txt atualizado
pip freeze > requirements.txt

# Criar Procfile
echo "web: gunicorn ecommerce.wsgi --log-file -" > Procfile

# Instalar gunicorn
pip install gunicorn
pip freeze > requirements.txt
```

#### 2. Configurar Railway

1. Acesse [railway.app](https://railway.app)
2. Conecte seu GitHub
3. Clique em "New Project" → "Deploy from GitHub repo"
4. Selecione o repositório do backend
5. Railway detecta automaticamente Django

#### 3. Configurar Variáveis de Ambiente

No Railway Dashboard, adicione:

```env
DEBUG=False
SECRET_KEY=seu-secret-key-super-seguro-aqui
ALLOWED_HOSTS=seu-app.railway.app
DATABASE_URL=postgresql://... (Railway cria automaticamente)
DJANGO_SETTINGS_MODULE=ecommerce.settings
```

#### 4. Configurar PostgreSQL

1. No Railway, clique em "New" → "Database" → "PostgreSQL"
2. Railway conecta automaticamente via `DATABASE_URL`

#### 5. Rodar Migrações

No Railway, vá em "Settings" → "Deploy" → "Custom Start Command":

```bash
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ecommerce.wsgi
```

### Opção B: Render

#### 1. Criar conta no Render

1. Acesse [render.com](https://render.com)
2. Conecte GitHub

#### 2. Criar Web Service

1. "New" → "Web Service"
2. Conecte repositório
3. Configurações:
   - **Name**: sportgear-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn ecommerce.wsgi:application`

#### 3. Variáveis de Ambiente

```env
PYTHON_VERSION=3.11
DEBUG=False
SECRET_KEY=seu-secret-key
ALLOWED_HOSTS=sportgear-api.onrender.com
DATABASE_URL=postgresql://...
```

#### 4. Adicionar PostgreSQL

1. "New" → "PostgreSQL"
2. Copiar `DATABASE_URL` para o Web Service

---

## 🎨 PARTE 2: DEPLOY DO FRONTEND (Next.js)

### Vercel (Recomendado)

#### 1. Preparar Frontend

```bash
cd c:\ecommerce\frontend

# Testar build local
npm run build

# Se der erro, corrigir e testar novamente
```

#### 2. Deploy na Vercel

**Opção 1: Via CLI**

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Deploy para produção
vercel --prod
```

**Opção 2: Via Dashboard**

1. Acesse [vercel.com](https://vercel.com)
2. "Add New" → "Project"
3. Importe repositório do GitHub
4. Vercel detecta Next.js automaticamente
5. Clique em "Deploy"

#### 3. Configurar Variáveis de Ambiente

No Vercel Dashboard → Settings → Environment Variables:

```env
NEXT_PUBLIC_API_URL=https://seu-backend.railway.app
NEXT_PUBLIC_APP_NAME=SportGear Premium
NEXT_PUBLIC_APP_URL=https://seu-app.vercel.app
```

#### 4. Redeployar

Após adicionar variáveis, clique em "Redeploy" no dashboard.

---

## 🔧 PARTE 3: CONFIGURAÇÕES FINAIS

### 1. Atualizar CORS no Backend

No `settings.py` do Django:

```python
CORS_ALLOWED_ORIGINS = [
    "https://seu-app.vercel.app",
    "http://localhost:3000",  # Para desenvolvimento
]
```

Redeploy o backend após essa mudança.

### 2. Atualizar ALLOWED_HOSTS

```python
ALLOWED_HOSTS = [
    'seu-app.railway.app',
    'localhost',
    '127.0.0.1',
]
```

### 3. Configurar HTTPS

Ambos Railway e Vercel fornecem HTTPS automaticamente.

No Django `settings.py`:

```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
```

---

## ✅ PARTE 4: VERIFICAÇÃO

### Testar Backend

```bash
# Testar API
curl https://seu-backend.railway.app/api/produtos/

# Deve retornar 401 (precisa de autenticação) ou lista de produtos
```

### Testar Frontend

1. Acesse `https://seu-app.vercel.app`
2. Navegue pelas páginas
3. Teste login
4. Adicione produto ao carrinho
5. Finalize compra

### Checklist Final

- [ ] Backend rodando sem erros
- [ ] Frontend carrega corretamente
- [ ] Login funciona
- [ ] Produtos aparecem
- [ ] Carrinho funciona
- [ ] Checkout completa
- [ ] CORS configurado
- [ ] HTTPS ativo
- [ ] Variáveis de ambiente corretas

---

## 🐛 TROUBLESHOOTING

### Erro: CORS

**Problema**: Frontend não consegue acessar backend

**Solução**:
1. Verifique `CORS_ALLOWED_ORIGINS` no backend
2. Adicione domínio do Vercel
3. Redeploy backend

### Erro: 500 Internal Server Error

**Problema**: Backend com erro

**Solução**:
1. Verifique logs no Railway/Render
2. Confirme `DEBUG=False`
3. Verifique `SECRET_KEY` está definida
4. Rode migrações: `python manage.py migrate`

### Erro: Build Failed (Frontend)

**Problema**: Build do Next.js falha

**Solução**:
1. Rode `npm run build` localmente
2. Corrija erros TypeScript
3. Verifique imports
4. Commit e push novamente

### Erro: Database Connection

**Problema**: Backend não conecta ao PostgreSQL

**Solução**:
1. Verifique `DATABASE_URL` está definida
2. Confirme formato: `postgresql://user:pass@host:port/db`
3. Teste conexão manualmente

---

## 📊 MONITORAMENTO

### Railway

- Dashboard mostra logs em tempo real
- Métricas de CPU/RAM
- Histórico de deploys

### Vercel

- Analytics integrado
- Logs de build e runtime
- Performance metrics

### Recomendações

- Configure alertas de erro
- Monitore uso de recursos
- Faça backups regulares do banco

---

## 🔄 ATUALIZAÇÕES

### Atualizar Backend

```bash
# Fazer mudanças no código
git add .
git commit -m "Update: descrição"
git push origin main

# Railway/Render fazem redeploy automático
```

### Atualizar Frontend

```bash
# Fazer mudanças no código
git add .
git commit -m "Update: descrição"
git push origin main

# Vercel faz redeploy automático
```

---

## 💰 CUSTOS ESTIMADOS

### Tier Gratuito

- **Vercel**: Grátis (Hobby plan)
- **Railway**: $5/mês de crédito grátis
- **Render**: Grátis (com limitações)

### Produção

- **Vercel Pro**: $20/mês
- **Railway**: ~$10-20/mês
- **Render**: ~$7-25/mês

---

## 📚 RECURSOS ADICIONAIS

- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)

---

## 🎉 CONCLUSÃO

Após seguir este guia, você terá:

✅ Backend Django rodando em produção  
✅ Frontend Next.js acessível globalmente  
✅ Banco PostgreSQL configurado  
✅ HTTPS ativo  
✅ Deploy automático via Git  

**Seu e-commerce está pronto para o mundo! 🚀**
