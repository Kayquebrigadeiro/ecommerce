# 🔐 Configuração de Secrets para CI/CD

## GitHub Secrets Necessários

Para que o pipeline de CI/CD funcione corretamente, você precisa configurar os seguintes secrets no GitHub:

### 1. Acessar Configurações de Secrets
1. Vá para o repositório no GitHub
2. Clique em **Settings** > **Secrets and variables** > **Actions**
3. Clique em **New repository secret**

### 2. Secrets Obrigatórios

#### AWS Credentials
```
AWS_ACCESS_KEY_ID
Descrição: Access Key ID da sua conta AWS
Exemplo: AKIAIOSFODNN7EXAMPLE
```

```
AWS_SECRET_ACCESS_KEY
Descrição: Secret Access Key da sua conta AWS
Exemplo: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

```
AWS_REGION
Descrição: Região AWS onde o Elastic Beanstalk está configurado
Exemplo: us-east-1
Opções: us-east-1, us-west-2, sa-east-1, etc.
```

#### Elastic Beanstalk Configuration
```
EB_APP_NAME
Descrição: Nome da aplicação no Elastic Beanstalk
Exemplo: ecommerce-api
```

```
EB_ENV_NAME
Descrição: Nome do ambiente no Elastic Beanstalk
Exemplo: ecommerce-api-prod
```

### 3. Secrets Opcionais (Recomendados)

```
DJANGO_SECRET_KEY
Descrição: Secret key do Django para produção
Como gerar: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```
DATABASE_URL
Descrição: URL de conexão com o banco de dados PostgreSQL
Exemplo: postgres://user:password@host:5432/dbname
```

---

## 📋 Checklist de Configuração

### Antes do Primeiro Deploy
- [ ] Criar conta AWS
- [ ] Configurar IAM user com permissões:
  - `AWSElasticBeanstalkFullAccess`
  - `AmazonEC2FullAccess`
  - `AmazonS3FullAccess`
- [ ] Criar aplicação no Elastic Beanstalk
- [ ] Criar ambiente (staging ou production)
- [ ] Configurar RDS PostgreSQL (opcional)
- [ ] Adicionar todos os secrets no GitHub
- [ ] Testar pipeline em branch de teste primeiro

### Configuração do Elastic Beanstalk

#### 1. Criar Aplicação
```bash
eb init ecommerce-api --region us-east-1 --platform "Python 3.11"
```

#### 2. Criar Ambiente
```bash
eb create ecommerce-api-prod --database.engine postgres --database.username dbuser
```

#### 3. Configurar Variáveis de Ambiente no EB
```bash
eb setenv \
  DEBUG=False \
  SECRET_KEY=your-secret-key \
  ALLOWED_HOSTS=.elasticbeanstalk.com \
  DATABASE_NAME=ebdb \
  DATABASE_USER=dbuser \
  DATABASE_PASSWORD=your-db-password \
  DATABASE_HOST=your-rds-endpoint \
  DATABASE_PORT=5432
```

#### 4. Configurar HTTPS (Recomendado)
- Adicionar certificado SSL via AWS Certificate Manager
- Configurar Load Balancer para usar HTTPS
- Redirecionar HTTP para HTTPS

---

## 🚀 Como Funciona o Pipeline

### 1. Test and Lint Job
```yaml
Triggers: Push ou Pull Request na branch main
Steps:
  1. Checkout do código
  2. Setup Python 3.14
  3. Cache de dependências
  4. Instalar dependências
  5. Aguardar PostgreSQL
  6. Rodar migrations
  7. Rodar flake8 (lint)
  8. Rodar testes com coverage
  9. Upload de relatório de cobertura
```

### 2. Deploy Job
```yaml
Triggers: Push na branch main (após testes passarem)
Steps:
  1. Checkout do código
  2. Setup Python 3.14
  3. Instalar EB CLI
  4. Configurar credenciais AWS
  5. Inicializar EB e fazer deploy
  6. Rodar migrations no EB
  7. Coletar arquivos estáticos
  8. Notificação de sucesso
```

---

## 🔧 Troubleshooting

### Erro: "AWS credentials not found"
**Solução:** Verifique se os secrets `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` estão configurados corretamente.

### Erro: "EB environment not found"
**Solução:** Certifique-se de que `EB_APP_NAME` e `EB_ENV_NAME` correspondem aos nomes reais no Elastic Beanstalk.

### Erro: "Tests failed"
**Solução:** Rode os testes localmente primeiro: `python manage.py test`

### Erro: "Migrations failed on EB"
**Solução:** Rode migrations manualmente via EB console:
```bash
eb ssh
source /var/app/venv/*/bin/activate
python manage.py migrate
```

---

## 📊 Monitoramento

### Logs do Pipeline
- Acesse: GitHub > Actions > Selecione o workflow
- Visualize logs de cada step
- Baixe artifacts se disponíveis

### Logs do Elastic Beanstalk
```bash
# Ver logs em tempo real
eb logs --stream

# Baixar logs
eb logs
```

### Health Check
```bash
# Verificar status do ambiente
eb status

# Abrir aplicação no browser
eb open
```

---

## 🎯 Próximos Passos

1. **Configurar Staging Environment**
   - Criar ambiente separado para testes
   - Configurar deploy automático para staging em PRs

2. **Adicionar Notificações**
   - Slack/Discord para notificar deploys
   - Email para falhas no pipeline

3. **Implementar Blue-Green Deployment**
   - Zero downtime deployments
   - Rollback automático em caso de falha

4. **Adicionar Testes de Integração**
   - Smoke tests após deploy
   - Health checks automatizados

---

**Última atualização:** 29/01/2026  
**Documentação:** Amazon Q + Desenvolvedor
