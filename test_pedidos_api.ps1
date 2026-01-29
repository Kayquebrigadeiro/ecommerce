# Script de teste da API de Pedidos
# PowerShell version

Write-Host "=== TESTE DA API DE PEDIDOS ===" -ForegroundColor Cyan

# 1. Obter token JWT
Write-Host "`n1. Obtendo token JWT..." -ForegroundColor Yellow
$loginBody = @{
    username = "kayquebrigadeiro"
    password = "senha123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/token/" `
        -Headers @{ "Content-Type" = "application/json" } `
        -Body $loginBody
    
    $accessToken = $response.access
    Write-Host "✅ Token obtido com sucesso!" -ForegroundColor Green
    Write-Host "Access Token: $($accessToken.Substring(0, 50))..." -ForegroundColor Gray
} catch {
    Write-Host "❌ Erro ao obter token: $_" -ForegroundColor Red
    exit
}

# 2. Listar pedidos do usuário autenticado
Write-Host "`n2. Listando meus pedidos..." -ForegroundColor Yellow
try {
    $pedidos = Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/api/meus-pedidos/" `
        -Headers @{ "Authorization" = "Bearer $accessToken" }
    
    Write-Host "✅ Pedidos encontrados: $($pedidos.Count)" -ForegroundColor Green
    $pedidos | ConvertTo-Json -Depth 3
} catch {
    Write-Host "❌ Erro ao listar pedidos: $_" -ForegroundColor Red
}

# 3. Criar novo pedido
Write-Host "`n3. Criando novo pedido..." -ForegroundColor Yellow
$novoPedido = @{
    status = "pendente"
    total = "149.90"
} | ConvertTo-Json

try {
    $pedidoCriado = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/pedidos/" `
        -Headers @{ 
            "Authorization" = "Bearer $accessToken"
            "Content-Type" = "application/json"
        } `
        -Body $novoPedido
    
    Write-Host "✅ Pedido criado com sucesso!" -ForegroundColor Green
    $pedidoCriado | ConvertTo-Json -Depth 3
    $pedidoId = $pedidoCriado.id
} catch {
    Write-Host "⚠️ Endpoint /api/pedidos/ não disponível (normal se não estiver no router)" -ForegroundColor Yellow
    Write-Host "Detalhes: $_" -ForegroundColor Gray
}

# 4. Listar todos os pedidos (se disponível)
Write-Host "`n4. Listando todos os pedidos..." -ForegroundColor Yellow
try {
    $todosPedidos = Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/api/pedidos/" `
        -Headers @{ "Authorization" = "Bearer $accessToken" }
    
    Write-Host "✅ Total de pedidos: $($todosPedidos.Count)" -ForegroundColor Green
    $todosPedidos | ConvertTo-Json -Depth 3
} catch {
    Write-Host "⚠️ Endpoint /api/pedidos/ não disponível" -ForegroundColor Yellow
}

Write-Host "`n=== TESTE CONCLUÍDO ===" -ForegroundColor Cyan
