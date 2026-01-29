# 🔍 Guia de Verificação Pós-Deploy

## 📋 Checklist de Verificação Imediata

### 1. ✅ Console AWS - Elastic Beanstalk

#### Verificar Status do Environment
```
AWS Console > Elastic Beanstalk > Environments

Verificar:
- [ ] Environment aparece na lista
- [ ] Status: Green (Ok) / Yellow (Warning) / Red (Severe)
- [ ] Health: Ok / Warning / Degraded / Severe
- [ ] Running Version: Versão mais recente deployada
```

#### Verificar Health e Events
```
Environment > Health
- [ ] Todas as instâncias EC2 estão "Ok"
- [ ] Requests: sem erros 5xx
- [ ] CPU/Memory: dentro dos limites

Environment > Events (últimos 30 minutos)
- [ ] Sem erros de deploy
- [ ] Sem falhas de health checks
- [ ] Sem problemas com dependências
```

#### Verificar Logs
```
Environment > Logs > Request Logs > Last 100 Lines

Procurar por:
- ❌ Tracebacks do Django
- ❌ ModuleNotFoundError
- ❌ Database connection errors
- ❌ Permission denied
- ✅ "Starting gunicorn" ou "Booting worker"
```

### 2. ✅ RDS (Se usar banco PostgreSQL)

```
AWS Console > RDS > Databases

Verificar:
- [ ] Status: Available
- [ ] Endpoint correto (copiar para comparar com DATABASE_HOST)
- [ ] Port: 5432
- [ ] VPC Security Group permite conexões do EB
```

### 3. ✅ EC2 / Security Groups

```
AWS Console > EC2 > Security Groups

Verificar:
- [ ] Security Group do EB permite HTTP (80) e HTTPS (443)
- [ ] Security Group do RDS permite PostgreSQL (5432) do SG do EB
- [ ] Inbound rules configuradas corretamente
```

### 4. ✅ S3 (Elastic Beanstalk Storage)

```
AWS Console > S3 > Buckets

Verificar:
- [ ] Bucket elasticbeanstalk-{region}-{account-id} existe
- [ ] Contém objetos do deploy recente
- [ ] Versões da aplicação estão armazenadas
```

---

## 🖥️ Comandos EB CLI (Verificação Rápida)

### Instalar EB CLI (se necessário)
```bash
pip install awsebcli
```

### Comandos de Verificação
```bash
# 1. Ver status do environment
eb status

# 2. Ver saúde das instâncias
eb health

# 3. Ver logs completos
eb logs --all

# 4. Ver últimos 100 eventos
eb events

# 5. Ver configuração do environment
eb config

# 6. Abrir aplicação no browser
eb open

# 7. SSH no servidor
eb ssh
```

### Script PowerShell de Verificação Completa
```powershell
# Salvar como: verify_deployment.ps1

Write-Host "=== VERIFICAÇÃO DE DEPLOY ===" -ForegroundColor Cyan

# 1. Status
Write-Host "`n1. Verificando status..." -ForegroundColor Yellow
eb status

# 2. Health
Write-Host "`n2. Verificando saúde..." -ForegroundColor Yellow
eb health

# 3. Últimos eventos
Write-Host "`n3. Últimos eventos..." -ForegroundColor Yellow
eb events | Select-Object -First 20

# 4. Logs recentes
Write-Host "`n4. Logs recentes..." -ForegroundColor Yellow
eb logs --stream

Write-Host "`n=== VERIFICAÇÃO CONCLUÍDA ===" -ForegroundColor Cyan
```

---

## 🔧 Verificações no Django (Pós-Deploy)

### Via EB Console > Configuration > Software > Run Command

#### 1. Verificar Python e Dependências
```bash
python --version
pip freeze | grep -i django
pip freeze | grep -i djangorestframework
```

#### 2. Rodar Migrations
```bash
source /var/app/venv/*/bin/activate
python manage.py migrate --noinput
```

#### 3. Coletar Arquivos Estáticos
```bash
source /var/app/venv/*/bin/activate
python manage.py collectstatic --noinput
```

#### 4. Verificar Configuração do Django
```bash
source /var/app/venv/*/bin/activate
python manage.py check
python manage.py showmigrations
```

#### 5. Criar Superuser (se necessário)
```bash
source /var/app/venv/*/bin/activate
python manage.py createsuperuser --noinput \
  --username admin \
  --email admin@example.com
```

### Via SSH (eb ssh)
```bash
# Conectar
eb ssh

# Ativar virtualenv
source /var/app/venv/*/bin/activate

# Navegar para diretório da aplicação
cd /var/app/current

# Rodar comandos Django
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check

# Ver logs em tempo real
tail -f /var/log/web.stdout.log

# Sair
exit
```

---

## ⚠️ Problemas Comuns e Soluções

### 1. Health Checks Falhando (Status: Severe)

**Sintomas:**
- Environment em status Red/Severe
- Instâncias EC2 sendo recriadas constantemente

**Verificar:**
```bash
# Ver logs
eb logs --all | grep -i "health"

# Verificar ALLOWED_HOSTS
eb printenv | grep ALLOWED_HOSTS
```

**Solução:**
```bash
# Adicionar domínio do EB ao ALLOWED_HOSTS
eb setenv ALLOWED_HOSTS=".elasticbeanstalk.com,localhost,127.0.0.1"
```

### 2. Erro 500 no Browser

**Verificar:**
```bash
# Ver logs do Django
eb logs --all | grep -i "error\|exception\|traceback"
```

**Soluções Comuns:**
```bash
# 1. SECRET_KEY faltando
eb setenv SECRET_KEY="sua-secret-key-aqui"

# 2. DEBUG=True em produção (não recomendado)
eb setenv DEBUG=False

# 3. Migrations não aplicadas
eb ssh
source /var/app/venv/*/bin/activate
python manage.py migrate
```

### 3. Erro de Conexão com Banco de Dados

**Sintomas:**
- "OperationalError: could not connect to server"
- "FATAL: password authentication failed"

**Verificar:**
```bash
# Ver variáveis de ambiente
eb printenv | grep DATABASE

# Testar conexão do servidor
eb ssh
telnet your-rds-endpoint.rds.amazonaws.com 5432
```

**Solução:**
```bash
# Configurar variáveis corretas
eb setenv \
  DATABASE_NAME=ebdb \
  DATABASE_USER=postgres \
  DATABASE_PASSWORD=sua-senha \
  DATABASE_HOST=seu-endpoint.rds.amazonaws.com \
  DATABASE_PORT=5432

# Verificar Security Group do RDS
# AWS Console > RDS > Database > Connectivity & security > VPC security groups
# Adicionar regra: PostgreSQL (5432) do Security Group do EB
```

### 4. Arquivos Estáticos Faltando (404 em CSS/JS)

**Sintomas:**
- Página carrega mas sem estilos
- Admin do Django sem CSS

**Solução:**
```bash
# Via SSH
eb ssh
source /var/app/venv/*/bin/activate
python manage.py collectstatic --noinput

# Verificar se STATIC_ROOT está configurado
python manage.py diffsettings | grep STATIC
```

### 5. Dependência Faltando no Build

**Sintomas:**
- Deploy falha com "ModuleNotFoundError"
- Logs mostram "No module named 'xxx'"

**Solução:**
```bash
# Localmente, atualizar requirements.txt
pip freeze > requirements.txt

# Verificar se o pacote está listado
cat requirements.txt | grep nome-do-pacote

# Fazer novo deploy
git add requirements.txt
git commit -m "fix: Add missing dependency"
git push origin main
```

### 6. Timeout no Deploy

**Sintomas:**
- Deploy demora mais de 10 minutos
- Timeout error no GitHub Actions

**Solução:**
```bash
# Aumentar timeout no EB
# AWS Console > EB > Configuration > Software > Command timeout
# Aumentar de 300s para 600s ou mais

# Ou via CLI
eb config
# Procurar por "Timeout" e aumentar o valor
```

---

## 📊 Verificação via GitHub Actions

### Ver Logs do Pipeline
```
1. GitHub > Actions
2. Selecionar o workflow mais recente
3. Clicar no job "deploy"
4. Expandir cada step para ver logs
```

### Comandos para Debug Local
```bash
# Ver último run
gh run list --workflow=ci.yml --limit 1

# Ver logs do último run
gh run view --log

# Re-executar workflow falhado
gh run rerun <run-id>
```

---

## ✅ Checklist de Verificação Completa

### Pré-Deploy
- [ ] Secrets configurados no GitHub
- [ ] EB Application criada
- [ ] EB Environment criado
- [ ] RDS configurado (se usar)
- [ ] Security Groups configurados

### Pós-Deploy
- [ ] Environment status: Green
- [ ] Health checks: Ok
- [ ] Logs sem erros críticos
- [ ] Aplicação abre no browser
- [ ] API responde corretamente
- [ ] Admin do Django acessível
- [ ] Banco de dados conectado
- [ ] Arquivos estáticos carregando

### Testes Funcionais
- [ ] Login funciona
- [ ] Criar pedido funciona
- [ ] Listar pedidos funciona
- [ ] JWT tokens funcionam
- [ ] CORS configurado corretamente

---

## 🚨 Comandos de Emergência

### Rollback para Versão Anterior
```bash
# Via Console
# EB > Environment > Actions > Restore previous version

# Via CLI
eb deploy --version <version-label>
```

### Reiniciar Environment
```bash
# Via Console
# EB > Environment > Actions > Restart app server(s)

# Via CLI
eb restart
```

### Ver Logs em Tempo Real
```bash
eb logs --stream
```

### Forçar Novo Deploy
```bash
# Mesmo código, nova tentativa
eb deploy --staged
```

---

## 📞 Suporte e Próximos Passos

### Se Tudo Funcionou ✅
1. Testar todos os endpoints da API
2. Criar superuser para admin
3. Configurar domínio customizado
4. Configurar HTTPS/SSL
5. Configurar monitoramento (CloudWatch)
6. Configurar backups automáticos

### Se Algo Falhou ❌
1. Copiar logs completos: `eb logs --all > logs.txt`
2. Copiar eventos: `eb events > events.txt`
3. Copiar configuração: `eb config > config.txt`
4. Compartilhar arquivos para análise

---

**Última atualização:** 29/01/2026  
**Mantido por:** DevOps Team
