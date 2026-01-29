# 🔧 CI/CD Troubleshooting Guide

## ⚠️ Problemas Comuns e Soluções

### 1. "AWS credentials not found"
**Causa:** Secrets do GitHub não configurados corretamente

**Solução:**
```bash
# Verificar se os secrets estão configurados:
# GitHub > Settings > Secrets and variables > Actions

Secrets obrigatórios:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- EB_APP_NAME
- EB_ENV_NAME
```

### 2. "EB application not found"
**Causa:** Aplicação não existe no Elastic Beanstalk

**Solução:**
```bash
# Criar aplicação localmente primeiro:
eb init ecommerce-api --region us-east-1 --platform "Python 3.11"
eb create ecommerce-api-prod

# Ou criar via AWS Console:
# Elastic Beanstalk > Create Application
```

### 3. "Permission denied" no deploy
**Causa:** IAM user sem permissões suficientes

**Solução:**
```
Adicionar policies ao IAM user:
- AWSElasticBeanstalkFullAccess
- AmazonS3FullAccess
- AmazonEC2FullAccess
- CloudFormationFullAccess
```

### 4. "eb ssh failed" no pipeline
**Causa:** SSH não configurado no EB ou runner não tem acesso

**Solução:**
```bash
# Opção 1: Rodar migrations manualmente via EB Console
# EB Console > Environment > Actions > Run command
python manage.py migrate --noinput

# Opção 2: SSH manual
eb ssh
source /var/app/venv/*/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

### 5. "Tests failed" no pipeline
**Causa:** Testes falhando no CI

**Solução:**
```bash
# Rodar testes localmente primeiro:
python manage.py test

# Com mais detalhes:
python manage.py test --verbosity=2

# Verificar se PostgreSQL está rodando no CI
# (já configurado no workflow)
```

### 6. "Module not found" no EB
**Causa:** Dependência faltando no requirements.txt

**Solução:**
```bash
# Regenerar requirements.txt:
pip freeze > requirements.txt

# Verificar se todas as dependências estão listadas:
cat requirements.txt | grep django
cat requirements.txt | grep djangorestframework
```

### 7. "Database connection failed" no EB
**Causa:** Variáveis de ambiente não configuradas

**Solução:**
```bash
# Configurar variáveis no EB:
eb setenv \
  DEBUG=False \
  SECRET_KEY=your-secret-key \
  DATABASE_NAME=ebdb \
  DATABASE_USER=dbuser \
  DATABASE_PASSWORD=your-password \
  DATABASE_HOST=your-rds-endpoint.rds.amazonaws.com \
  DATABASE_PORT=5432 \
  ALLOWED_HOSTS=.elasticbeanstalk.com
```

### 8. "Static files not found" (404 em CSS/JS)
**Causa:** collectstatic não executado

**Solução:**
```bash
# Via SSH:
eb ssh
source /var/app/venv/*/bin/activate
python manage.py collectstatic --noinput

# Ou adicionar em .ebextensions/django.config:
container_commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && python manage.py migrate --noinput"
  02_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput"
```

---

## 📋 Checklist Pré-Deploy

### Antes do Primeiro Deploy
- [ ] Criar conta AWS
- [ ] Criar IAM user com permissões necessárias
- [ ] Gerar Access Key e Secret Key
- [ ] Criar aplicação no Elastic Beanstalk
- [ ] Criar ambiente (staging/production)
- [ ] Configurar RDS PostgreSQL (opcional)
- [ ] Adicionar todos os secrets no GitHub
- [ ] Testar pipeline em branch de teste

### Configuração do GitHub
- [ ] Secrets configurados corretamente
- [ ] Workflow file em `.github/workflows/ci.yml`
- [ ] Branch protection rules (opcional)
- [ ] Notifications configuradas (opcional)

### Configuração do Elastic Beanstalk
- [ ] Aplicação criada
- [ ] Ambiente criado
- [ ] Variáveis de ambiente configuradas
- [ ] RDS configurado (se usar)
- [ ] Security groups configurados
- [ ] Load balancer configurado
- [ ] HTTPS configurado (recomendado)

---

## 🚀 Comandos Úteis

### Elastic Beanstalk CLI
```bash
# Ver status do ambiente
eb status

# Ver logs em tempo real
eb logs --stream

# Baixar logs
eb logs

# Abrir aplicação no browser
eb open

# SSH no servidor
eb ssh

# Configurar variável de ambiente
eb setenv KEY=value

# Listar ambientes
eb list

# Trocar de ambiente
eb use environment-name
```

### Debugging no EB
```bash
# SSH e ativar virtualenv
eb ssh
source /var/app/venv/*/bin/activate

# Ver logs do Django
tail -f /var/log/web.stdout.log

# Ver logs do EB
tail -f /var/log/eb-engine.log

# Testar manage.py commands
python manage.py check
python manage.py showmigrations
python manage.py migrate --plan
```

### GitHub Actions
```bash
# Ver workflows
gh workflow list

# Ver runs de um workflow
gh run list --workflow=ci.yml

# Ver logs de um run
gh run view <run-id> --log

# Re-run um workflow
gh run rerun <run-id>
```

---

## 📊 Monitoramento

### Logs do Pipeline
- GitHub > Actions > Selecione o workflow
- Clique no job para ver logs detalhados
- Baixe artifacts se disponíveis

### Logs do Elastic Beanstalk
```bash
# Logs em tempo real
eb logs --stream

# Logs específicos
eb logs --log-group /aws/elasticbeanstalk/environment-name/var/log/web.stdout.log
```

### Health Monitoring
```bash
# Status do ambiente
eb health

# Métricas detalhadas
eb health --refresh
```

---

## 🔄 Rollback

### Se o deploy falhar:
```bash
# Via EB Console
# Environment > Actions > Restore previous version

# Via CLI
eb deploy --version previous-version-label
```

### Se precisar reverter código:
```bash
# Git revert
git revert HEAD
git push origin main

# Ou force push (cuidado!)
git reset --hard HEAD~1
git push --force origin main
```

---

## 📞 Suporte

### Recursos Úteis
- [AWS Elastic Beanstalk Docs](https://docs.aws.amazon.com/elasticbeanstalk/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

### Logs para Análise
Ao reportar problemas, inclua:
1. Logs do GitHub Actions
2. Logs do EB (`eb logs`)
3. Configuração do ambiente (`eb config`)
4. Versão do Python e dependências

---

**Última atualização:** 29/01/2026  
**Mantido por:** Equipe de DevOps
