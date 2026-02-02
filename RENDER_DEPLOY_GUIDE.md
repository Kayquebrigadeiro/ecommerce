# 🚀 Guia Completo de Deploy no Render

## 📋 Pré-requisitos
- ✅ Projeto no GitHub (já feito)
- ✅ Conta no Render (criar em https://render.com)

---

## 🎯 Passo 1: Criar Banco de Dados PostgreSQL

### 1.1 No Render Dashboard
1. Clique em **New +** → **PostgreSQL**
2. Preencha:
   - **Name:** `ecommerce-db`
   - **Database:** `ecommerce`
   - **User:** `ecommerce_user` (ou deixe padrão)
   - **Region:** Oregon (US West) - mais próximo
   - **Plan:** Free
3. Clique em **Create Database**

### 1.2 Copiar Credenciais
Após criar, copie as informações:
- **Internal Database URL** (use esta!)
- Ou copie individualmente:
  - Hostname
  - Port
  - Database
  - Username
  - Password

---

## 🎯 Passo 2: Criar Web Service

### 2.1 No Render Dashboard
1. Clique em **New +** → **Web Service**
2. Conecte seu repositório GitHub
3. Selecione o repositório: `Kayquebrigadeiro/ecommerce`

### 2.2 Configurar o Service
```
Name: ecommerce-api
Region: Oregon (US West)
Branch: main
Root Directory: (deixe vazio)
Runtime: Python 3
Build Command: ./build.sh
Start Command: gunicorn ecommerce.wsgi:application
Plan: Free
```

---

## 🎯 Passo 3: Configurar Environment Variables

### 3.1 No Web Service → Environment
Adicione as seguintes variáveis:

#### Variáveis Obrigatórias:
```bash
# Django
SECRET_KEY=cole-sua-secret-key-aqui
DEBUG=False
ALLOWED_HOSTS=ecommerce-api.onrender.com,localhost

# Database (copie do PostgreSQL criado)
DATABASE_NAME=ecommerce
DATABASE_USER=ecommerce_user
DATABASE_PASSWORD=sua-senha-do-render
DATABASE_HOST=dpg-xxxxx.oregon-postgres.render.com
DATABASE_PORT=5432

# Email
EMAIL_FROM_USER=noreply@ecommerce.com

# Python
PYTHON_VERSION=3.11.0
```

#### Como Gerar SECRET_KEY:
```python
# Execute localmente:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.2 Salvar e Deploy
1. Clique em **Save Changes**
2. O deploy iniciará automaticamente

---

## 🎯 Passo 4: Verificar Deploy

### 4.1 Acompanhar Logs
- No Render Dashboard → Seu Service → **Logs**
- Aguarde mensagens:
  ```
  ==> Building...
  ==> Deploying...
  ==> Your service is live 🎉
  ```

### 4.2 Testar Aplicação
```bash
# Sua URL será algo como:
https://ecommerce-api.onrender.com

# Testar API
curl https://ecommerce-api.onrender.com/api/

# Testar admin
https://ecommerce-api.onrender.com/admin/
```

---

## 🎯 Passo 5: Criar Superuser

### 5.1 Via Render Shell
1. No Render Dashboard → Seu Service → **Shell**
2. Execute:
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (digite sua senha)
```

### 5.2 Acessar Admin
```
https://ecommerce-api.onrender.com/admin/
```

---

## 🔧 Comandos Úteis no Render Shell

### Rodar Migrations
```bash
python manage.py migrate
```

### Coletar Static Files
```bash
python manage.py collectstatic --noinput
```

### Ver Configurações
```bash
python manage.py check
python manage.py showmigrations
```

### Criar Dados de Teste
```bash
python manage.py shell
>>> from produtos.models import Produto
>>> from decimal import Decimal
>>> Produto.objects.create(nome="Produto Teste", preco=Decimal('99.90'), estoque=10)
```

---

## ⚠️ Troubleshooting

### Erro: "Application failed to respond"
**Solução:**
1. Verificar logs no Render
2. Confirmar que `gunicorn` está no requirements.txt
3. Verificar Start Command: `gunicorn ecommerce.wsgi:application`

### Erro: "Database connection failed"
**Solução:**
1. Verificar variáveis DATABASE_* no Environment
2. Usar **Internal Database URL** do PostgreSQL
3. Confirmar que DATABASE_HOST está correto

### Erro: "Static files not found"
**Solução:**
1. Verificar se WhiteNoise está instalado
2. Rodar no Shell: `python manage.py collectstatic --noinput`
3. Verificar STATIC_ROOT em settings.py

### Erro: "SECRET_KEY not set"
**Solução:**
1. Gerar nova SECRET_KEY
2. Adicionar em Environment Variables
3. Fazer redeploy

---

## 🎨 Configurar CORS para Frontend

### Se tiver frontend em outro domínio:
```python
# No Render Environment Variables, adicione:
CORS_ALLOWED_ORIGINS=https://seu-frontend.vercel.app,https://ecommerce-api.onrender.com
```

### Ou edite settings.py:
```python
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
```

---

## 📊 Monitoramento

### Ver Logs em Tempo Real
```
Render Dashboard → Service → Logs
```

### Ver Métricas
```
Render Dashboard → Service → Metrics
- CPU Usage
- Memory Usage
- Request Count
- Response Time
```

### Configurar Alertas
```
Render Dashboard → Service → Settings → Notifications
- Email on deploy failure
- Slack integration
```

---

## 🔄 Deploy Automático

### Configurado Automaticamente!
- Cada push na branch `main` dispara deploy automático
- Render detecta mudanças e faz rebuild
- Zero downtime deployment

### Desabilitar Auto-Deploy (opcional):
```
Service → Settings → Auto-Deploy
Toggle OFF
```

---

## 💰 Plano Free - Limitações

### O que está incluído:
- ✅ 750 horas/mês (suficiente para 1 serviço 24/7)
- ✅ 512 MB RAM
- ✅ PostgreSQL com 1 GB storage
- ✅ SSL/HTTPS automático
- ✅ Deploy automático do GitHub

### Limitações:
- ⚠️ Serviço "dorme" após 15 min de inatividade
- ⚠️ Primeiro request após sleep demora ~30s
- ⚠️ Banco de dados expira após 90 dias (free tier)

### Manter Serviço Ativo (opcional):
Use um serviço de ping como:
- UptimeRobot (https://uptimerobot.com)
- Cron-job.org (https://cron-job.org)

---

## 🚀 Upgrade para Plano Pago (opcional)

### Starter Plan ($7/mês):
- Sem sleep
- 1 GB RAM
- Melhor performance
- Banco de dados permanente

### Para Upgrade:
```
Service → Settings → Plan
Selecione "Starter" → Confirm
```

---

## 📝 Checklist Final

### Antes de Compartilhar:
- [ ] Aplicação acessível via HTTPS
- [ ] Admin funcionando
- [ ] API respondendo corretamente
- [ ] Superuser criado
- [ ] Dados de teste criados
- [ ] CORS configurado (se necessário)
- [ ] SSL/HTTPS ativo (automático no Render)

### URLs para Testar:
```
Homepage: https://ecommerce-api.onrender.com/
API Root: https://ecommerce-api.onrender.com/api/
Admin: https://ecommerce-api.onrender.com/admin/
Produtos: https://ecommerce-api.onrender.com/api/produtos/
Token: https://ecommerce-api.onrender.com/api/token/
```

---

## 🎯 Próximos Passos

### 1. Domínio Customizado (opcional)
```
Service → Settings → Custom Domain
Adicione: api.seudominio.com
Configure DNS no seu provedor
```

### 2. Configurar Email Real
```python
# Adicionar no Environment:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-app-password
```

### 3. Adicionar Monitoramento
- Sentry para error tracking
- Google Analytics
- Logs centralizados

---

## 📞 Suporte

### Documentação Oficial:
- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/

### Comunidade:
- Render Community: https://community.render.com
- Django Forum: https://forum.djangoproject.com

---

**🎉 Parabéns! Seu projeto está no ar!**

**Última atualização:** 29/01/2026
