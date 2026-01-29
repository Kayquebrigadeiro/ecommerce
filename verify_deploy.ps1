# Script de Verificação Rápida de Deploy
# PowerShell version

param(
    [string]$EnvName = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VERIFICAÇÃO DE DEPLOY - E-COMMERCE API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($EnvName -eq "") {
    Write-Host "`n⚠️  Uso: .\verify_deploy.ps1 -EnvName nome-do-environment" -ForegroundColor Yellow
    Write-Host "Exemplo: .\verify_deploy.ps1 -EnvName ecommerce-api-prod`n" -ForegroundColor Gray
    
    # Tentar listar environments
    Write-Host "Listando environments disponíveis..." -ForegroundColor Yellow
    try {
        eb list
    } catch {
        Write-Host "❌ EB CLI não instalado. Instale com: pip install awsebcli" -ForegroundColor Red
    }
    exit
}

# 1. STATUS
Write-Host "`n[1/6] Verificando STATUS do environment..." -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
try {
    eb status $EnvName
    Write-Host "✅ Status obtido com sucesso" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao obter status: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# 2. HEALTH
Write-Host "`n[2/6] Verificando SAÚDE das instâncias..." -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
try {
    eb health $EnvName
    Write-Host "✅ Health check concluído" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao verificar health: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# 3. EVENTOS RECENTES
Write-Host "`n[3/6] Verificando EVENTOS recentes..." -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
try {
    $events = eb events $EnvName | Select-Object -First 15
    $events
    Write-Host "✅ Eventos obtidos" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao obter eventos: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# 4. VARIÁVEIS DE AMBIENTE
Write-Host "`n[4/6] Verificando VARIÁVEIS DE AMBIENTE..." -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
try {
    Write-Host "Variáveis configuradas:" -ForegroundColor Gray
    eb printenv $EnvName | Select-String -Pattern "DEBUG|SECRET_KEY|DATABASE|ALLOWED_HOSTS"
    Write-Host "✅ Variáveis listadas" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao listar variáveis: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# 5. LOGS RECENTES
Write-Host "`n[5/6] Verificando LOGS recentes..." -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
try {
    Write-Host "Últimas 50 linhas de log:" -ForegroundColor Gray
    eb logs $EnvName | Select-Object -Last 50
    Write-Host "✅ Logs obtidos" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao obter logs: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# 6. TESTE DE CONECTIVIDADE
Write-Host "`n[6/6] Testando CONECTIVIDADE..." -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
try {
    $url = (eb status $EnvName | Select-String -Pattern "CNAME:").ToString().Split(":")[1].Trim()
    $fullUrl = "http://$url"
    
    Write-Host "Testando: $fullUrl" -ForegroundColor Gray
    $response = Invoke-WebRequest -Uri $fullUrl -Method Get -TimeoutSec 10 -UseBasicParsing
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Aplicação respondendo (Status: $($response.StatusCode))" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Aplicação respondeu com status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Erro ao testar conectividade: $_" -ForegroundColor Red
    Write-Host "Tente abrir manualmente: eb open $EnvName" -ForegroundColor Yellow
}

# RESUMO
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  VERIFICAÇÃO CONCLUÍDA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`n📋 Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Verificar logs completos: eb logs $EnvName --all" -ForegroundColor Gray
Write-Host "2. Abrir aplicação: eb open $EnvName" -ForegroundColor Gray
Write-Host "3. SSH no servidor: eb ssh $EnvName" -ForegroundColor Gray
Write-Host "4. Ver configuração: eb config $EnvName" -ForegroundColor Gray

Write-Host "`n🔧 Comandos úteis:" -ForegroundColor Yellow
Write-Host "- Rodar migrations: eb ssh $EnvName --command 'source /var/app/venv/*/bin/activate && python manage.py migrate'" -ForegroundColor Gray
Write-Host "- Collectstatic: eb ssh $EnvName --command 'source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput'" -ForegroundColor Gray
Write-Host "- Reiniciar: eb restart $EnvName" -ForegroundColor Gray
Write-Host "- Rollback: eb deploy $EnvName --version <version-label>`n" -ForegroundColor Gray
