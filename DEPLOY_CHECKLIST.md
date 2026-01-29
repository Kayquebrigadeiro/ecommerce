# 🚀 Checklist Pré-Deploy - E-Commerce API

## ✅ Verificações Imediatas

### Migrations e Testes
- [x] `python manage.py makemigrations` - Sem alterações pendentes
- [x] `python manage.py migrate` - Todas as migrations aplicadas
- [x] `python manage.py test pedidos` - **8 testes passando** (23.124s)
- [x] `python manage.py test usuarios` - 18 testes passando

### Cobertura de Testes
- [x] Casos de sucesso implementados
- [x] Casos de erro implementados
- [x] Casos de borda implementados:
  - [x] Quantidade inválida (< 1)
  - [x] Produto inexistente
  - [x] Isolamento entre usuários
  - [x] Autenticação obrigatória
- [ ] Gerar relatório de cobertura: `coverage run --source='.' manage.py test && coverage report`

### Testes de Integração Manual
- [x] Script PowerShell criado: `test_pedidos_api.ps1`
- [x] Autenticação JWT testada
- [x] Criação de pedidos testada
- [x] Listagem de pedidos testada
- [x] Atualização testada
- [x] Exclusão testada

---

## 🔒 Segurança e Configuração

### JWT
- [x] `ACCESS_TOKEN_LIFETIME` configurado (5 minutos)
- [x] `REFRESH_TOKEN_LIFETIME` configurado (24 horas)
- [x] Token blacklist habilitado
- [ ] `ROTATE_REFRESH_TOKENS = True` (recomendado para produção)
- [ ] `BLACKLIST_AFTER_ROTATION = True`

### Variáveis de Ambiente
- [x] `.env` criado com variáveis sensíveis
- [x] `.env` no `.gitignore`
- [x] `SECRET_KEY` em variável de ambiente
- [x] Credenciais do banco em variáveis de ambiente
- [ ] Criar `.env.example` para documentação

### Settings de Produção
- [ ] `DEBUG = False` em produção
- [ ] `ALLOWED_HOSTS` configurado
- [ ] `CSRF_TRUSTED_ORIGINS` configurado
- [ ] `CORS_ALLOWED_ORIGINS` configurado para domínio de produção
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SECURE_HSTS_SECONDS = 31536000`

### Permissões
- [x] `IsAuthenticated` em todos os endpoints de usuário
- [ ] `IsAdminUser` para endpoints administrativos
- [x] Filtragem por usuário no `get_queryset()`

---

## 🏗️ Estabilidade e Qualidade

### Transações
- [x] `transaction.atomic()` em criação de pedidos
- [x] `transaction.atomic()` em atualização de pedidos
- [x] Rollback automático em caso de erro

### Validações
- [x] Quantidade mínima (>= 1)
- [x] Produto deve existir
- [x] Pedido confirmado deve ter itens
- [x] Uso de `Decimal` para precisão monetária
- [ ] Validação de estoque disponível
- [ ] Normalização com `quantize()` para 2 casas decimais

### Banco de Dados
- [x] SQLite para desenvolvimento
- [x] PostgreSQL configurado para produção
- [ ] Índices otimizados
- [ ] Backup automático configurado
- [ ] Plano de rollback definido

---

## 🚀 Deploy e Infraestrutura

### Ambientes
- [x] Local configurado
- [ ] Staging configurado
- [ ] Produção configurada
- [ ] Testar migrations no staging antes de produção

### CI/CD
- [ ] Pipeline configurado (GitHub Actions / GitLab CI)
- [ ] Steps do pipeline:
  - [ ] Install dependencies
  - [ ] Run migrations (staging)
  - [ ] Run tests
  - [ ] Run lint (flake8)
  - [ ] Run type checking (mypy)
  - [ ] Deploy automático se tudo passar

### Monitoramento
- [ ] Logs centralizados (Sentry / Logstash)
- [ ] Métricas de performance
- [ ] Alertas para erros 5xx
- [ ] Alertas para falhas de jobs
- [ ] Health check endpoint

### Docker
- [ ] Dockerfile criado
- [ ] docker-compose.yml criado
- [ ] Imagem testada localmente
- [ ] Registry configurado

---

## 🌐 Integração com Frontend

### Endpoints
- [x] `/api/meus-pedidos/` - Listar pedidos do usuário
- [x] `/api/pedidos/` - CRUD completo
- [x] `/api/produtos/` - CRUD de produtos
- [x] `/api/token/` - Obter JWT
- [x] `/api/token/refresh/` - Renovar token
- [x] `/api/logout/` - Invalidar token
- [ ] Paginação implementada
- [ ] Filtros implementados (status, data)

### Documentação
- [ ] Swagger/Redoc implementado
- [ ] Exemplos de requisições documentados
- [ ] Códigos de erro documentados
- [ ] Rate limits documentados

### CORS
- [x] CORS configurado para localhost
- [ ] CORS configurado para domínio de produção
- [x] Credenciais habilitadas

---

## 📊 Métricas de Qualidade

### Testes
- ✅ **8/8 testes de pedidos passando**
- ✅ **18/18 testes de usuários passando**
- ✅ **Total: 26 testes passando**
- [ ] Cobertura mínima: 80%
- [ ] Testes de carga realizados

### Performance
- [ ] Queries otimizadas (select_related, prefetch_related)
- [ ] Cache implementado onde necessário
- [ ] Rate limiting configurado
- [ ] Tempo de resposta < 200ms (p95)

---

## 🔧 Tarefas Pendentes

### Alta Prioridade
1. [ ] Configurar variáveis de ambiente para produção
2. [ ] Implementar Swagger/Redoc
3. [ ] Criar Dockerfile e docker-compose
4. [ ] Configurar CI/CD básico
5. [ ] Implementar validação de estoque

### Média Prioridade
6. [ ] Adicionar paginação nos endpoints
7. [ ] Implementar filtros (status, data)
8. [ ] Configurar Sentry para monitoramento
9. [ ] Criar endpoint de health check
10. [ ] Adicionar rate limiting

### Baixa Prioridade
11. [ ] Implementar cache com Redis
12. [ ] Adicionar testes de carga
13. [ ] Otimizar queries com índices
14. [ ] Implementar webhooks para notificações
15. [ ] Adicionar suporte a múltiplos idiomas

---

## 📝 Comandos Úteis

### Desenvolvimento
```bash
# Rodar servidor
python manage.py runserver

# Rodar testes
python manage.py test

# Rodar testes com cobertura
coverage run --source='.' manage.py test
coverage report
coverage html

# Criar migrations
python manage.py makemigrations
python manage.py migrate

# Criar superuser
python manage.py createsuperuser
```

### Produção
```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Rodar com Gunicorn
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000

# Backup do banco
pg_dump ecommerce > backup_$(date +%Y%m%d).sql
```

---

**Última atualização:** 29/01/2026  
**Status:** ✅ Pronto para staging | ⚠️ Pendências para produção
