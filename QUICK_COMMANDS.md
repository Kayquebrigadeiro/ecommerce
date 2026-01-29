# 📋 Comandos Prontos - Copy & Paste

## 🚀 Verificação Rápida (5 minutos)

### 1. Status Geral
```bash
eb status
eb health
eb events | head -20
```

### 2. Ver Logs
```bash
# Últimas 100 linhas
eb logs | tail -100

# Logs em tempo real
eb logs --stream

# Todos os logs
eb logs --all > full_logs.txt
```

### 3. Abrir Aplicação
```bash
eb open
```

---

## 🔧 Correções Comuns (Copy & Paste)

### 1. Rodar Migrations
```bash
eb ssh
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py migrate --noinput
exit
```

### 2. Coletar Arquivos Estáticos
```bash
eb ssh
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py collectstatic --noinput
exit
```

### 3. Criar Superuser
```bash
eb ssh
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (digite sua senha)
exit
```

### 4. Verificar Configuração Django
```bash
eb ssh
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py check
python manage.py showmigrations
python manage.py diffsettings | grep -i "database\|secret\|debug\|allowed"
exit
```

---

## ⚙️ Configurar Variáveis de Ambiente

### Configuração Completa (Produção)
```bash
eb setenv \
  DEBUG=False \
  SECRET_KEY="cole-sua-secret-key-aqui" \
  ALLOWED_HOSTS=".elasticbeanstalk.com,seu-dominio.com" \
  DATABASE_NAME=ebdb \
  DATABASE_USER=postgres \
  DATABASE_PASSWORD="sua-senha-db" \
  DATABASE_HOST="seu-endpoint.rds.amazonaws.com" \
  DATABASE_PORT=5432 \
  EMAIL_FROM_USER="noreply@seu-dominio.com"
```

### Configuração Mínima (Teste)
```bash
eb setenv \
  DEBUG=False \
  SECRET_KEY="sua-secret-key" \
  ALLOWED_HOSTS=".elasticbeanstalk.com"
```

### Ver Variáveis Configuradas
```bash
eb printenv
```

---

## 🔍 Diagnóstico de Problemas

### Erro 500 - Ver Traceback
```bash
eb logs --all | grep -A 20 "Traceback"
```

### Erro de Banco - Testar Conexão
```bash
eb ssh
telnet seu-endpoint.rds.amazonaws.com 5432
# Se conectar: Ctrl+] depois "quit"
# Se não conectar: problema de Security Group
exit
```

### Verificar Dependências Instaladas
```bash
eb ssh
source /var/app/venv/*/bin/activate
pip freeze | grep -i django
pip freeze | grep -i rest
pip freeze | grep -i jwt
exit
```

### Ver Processos Rodando
```bash
eb ssh
ps aux | grep python
ps aux | grep gunicorn
exit
```

---

## 🔄 Operações de Deploy

### Forçar Novo Deploy
```bash
eb deploy --staged
```

### Rollback para Versão Anterior
```bash
# Listar versões
eb appversion

# Fazer rollback
eb deploy --version <version-label>
```

### Reiniciar Aplicação
```bash
eb restart
```

### Rebuild Environment
```bash
eb rebuild
```

---

## 📊 Monitoramento

### Ver Métricas em Tempo Real
```bash
eb health --refresh
```

### Ver Configuração Completa
```bash
eb config > eb_config.txt
cat eb_config.txt
```

### Baixar Todos os Logs
```bash
eb logs --all --zip
# Cria arquivo logs.zip
```

---

## 🧪 Testar API Após Deploy

### PowerShell
```powershell
# Obter URL do environment
$url = (eb status | Select-String -Pattern "CNAME:").ToString().Split(":")[1].Trim()
$baseUrl = "http://$url"

# Testar endpoint raiz
Invoke-RestMethod -Uri "$baseUrl/api/" -Method Get

# Testar login
$body = @{username="admin";password="sua-senha"} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "$baseUrl/api/token/" -Method Post -Body $body -ContentType "application/json"
$token = $response.access

# Testar endpoint protegido
Invoke-RestMethod -Uri "$baseUrl/api/produtos/" -Headers @{Authorization="Bearer $token"}
```

### Bash/Linux
```bash
# Obter URL
URL=$(eb status | grep CNAME | awk '{print $2}')
BASE_URL="http://$URL"

# Testar endpoint raiz
curl $BASE_URL/api/

# Testar login
TOKEN=$(curl -X POST $BASE_URL/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"sua-senha"}' \
  | jq -r '.access')

# Testar endpoint protegido
curl $BASE_URL/api/produtos/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🚨 Comandos de Emergência

### Aplicação Não Responde
```bash
# 1. Ver logs imediatamente
eb logs --stream

# 2. Reiniciar
eb restart

# 3. Se não resolver, rebuild
eb rebuild
```

### Erro de Memória/CPU
```bash
# Ver uso de recursos
eb health

# Escalar verticalmente (aumentar instância)
# AWS Console > EB > Configuration > Capacity > Instance type

# Escalar horizontalmente (mais instâncias)
eb scale 2
```

### Banco de Dados Travado
```bash
# Ver conexões ativas (via RDS)
# AWS Console > RDS > Database > Monitoring

# Reiniciar RDS (último recurso)
# AWS Console > RDS > Database > Actions > Reboot
```

---

## 📝 Checklist Rápido

### Após Cada Deploy
```bash
# 1. Verificar status
eb status

# 2. Ver últimos eventos
eb events | head -10

# 3. Testar aplicação
eb open

# 4. Ver logs por 1 minuto
timeout 60 eb logs --stream

# 5. Testar API
curl http://$(eb status | grep CNAME | awk '{print $2}')/api/
```

### Se Algo Falhar
```bash
# 1. Capturar evidências
eb logs --all > logs_$(date +%Y%m%d_%H%M%S).txt
eb events > events_$(date +%Y%m%d_%H%M%S).txt

# 2. Tentar correção rápida
eb restart

# 3. Se não resolver, rollback
eb deploy --version <versao-anterior>

# 4. Analisar logs offline
cat logs_*.txt | grep -i "error\|exception\|failed"
```

---

## 🎯 Comandos Mais Usados (Top 10)

```bash
1.  eb status                    # Ver status geral
2.  eb health                    # Ver saúde das instâncias
3.  eb logs --stream             # Logs em tempo real
4.  eb open                      # Abrir no browser
5.  eb ssh                       # Conectar via SSH
6.  eb restart                   # Reiniciar aplicação
7.  eb setenv KEY=value          # Configurar variável
8.  eb printenv                  # Ver variáveis
9.  eb deploy                    # Fazer deploy
10. eb events                    # Ver eventos recentes
```

---

**Dica:** Salve este arquivo e use como referência rápida!

**Última atualização:** 29/01/2026
