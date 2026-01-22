# Roadmap de Desenvolvimento - E-Commerce API

## ✅ Prioridade Imediata (CONCLUÍDA)

### Testes Automatizados
- ✅ 15 testes com APITestCase (registro, login, logout, refresh)
- ✅ Todos passando
- **Como rodar**: `python manage.py test usuarios`

### Recuperação de Senha
- ✅ `POST /api/password-reset/` - Requisição de reset
- ✅ `POST /api/password-reset-confirm/` - Confirmação com novo password
- ✅ Validação via PasswordResetTokenGenerator
- ✅ Envio de email (console backend em dev)

### Verificação de Email
- ✅ Campos `is_email_verified` e `email_verification_token` adicionados
- ✅ `POST /api/verify-email/` - Verificar email com token
- ✅ `POST /api/resend-verification/` - Reenviar token
- ✅ Email enviado automaticamente no registro

### CORS
- ✅ `django-cors-headers` instalado
- ✅ Configurado para `localhost:3000` e `localhost:8000`
- ✅ Credenciais ativadas

---

## 🔄 Segurança e Produção (PRÓXIMO NÍVEL)

### 5. Configurações de Produção
**Prioridade**: ALTA

Implementar variáveis de ambiente para:
- `ALLOWED_HOSTS` - Definir domínios permitidos
- `SECURE_SSL_REDIRECT = True` - Forçar HTTPS
- `SESSION_COOKIE_SECURE = True` - Cookies apenas em HTTPS
- `CSRF_COOKIE_SECURE = True` - CSRF apenas em HTTPS
- `SECURE_HSTS_SECONDS` - HSTS header

**Arquivo**: `settings.py` com `python-dotenv`

### 6. Banco em Produção - PostgreSQL
**Prioridade**: ALTA

- Instalar `psycopg2-binary`
- Configurar conexão PostgreSQL via variáveis de ambiente
- Migrar dados do SQLite para Postgres
- Adicionar pool de conexões

### 7. Docker + docker-compose
**Prioridade**: ALTA

- `Dockerfile` para Django
- `docker-compose.yml` com:
  - Django app
  - PostgreSQL
  - Redis (opcional para cache)
- Volumes para banco de dados
- Network configurada

---

## 📚 Documentação e DX

### 9. Documentação da API - Swagger
**Prioridade**: MÉDIA

- Instalar `drf-spectacular` ou `drf-yasg`
- Configurar endpoints Swagger/Redoc
- Documentar todos os endpoints
- Adicionar exemplos de requisição/resposta

**URLs**:
- `/api/schema/swagger-ui/`
- `/api/schema/redoc/`

### 10. Rate Limiting
**Prioridade**: MÉDIA

- Implementar throttling do DRF
- Configurar diferentes limits por endpoint
- Proteger `/api/token/` com rate limit stricter

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

---

## 🔍 Observabilidade e Robustez

### 8. CI/CD - GitHub Actions
**Prioridade**: MÉDIA

- Pipeline para rodar testes em cada push
- Linting (flake8, black)
- Coverage report
- Deploy automático (opcional)

`.github/workflows/tests.yml`

### 11. Logs e Monitoramento
**Prioridade**: MÉDIA

- Integração com Sentry para capturar erros
- Configurar logging de requests/responses
- Métricas básicas (Prometheus/Grafana)

### 12. Política de Tokens JWT
**Prioridade**: BAIXA

- Revisar tempos de expiração
- Implementar rotação de tokens (se necessário)
- Ajustar conforme UX

---

## Resumo de Tempo Estimado

| Tarefa | Dificuldade | Tempo Est. | Status |
|--------|-------------|-----------|--------|
| Testes | Média | 2h | ✅ Feito |
| Password Reset | Média | 1.5h | ✅ Feito |
| Email Verification | Média | 1.5h | ✅ Feito |
| CORS | Baixa | 30min | ✅ Feito |
| Produção | Alta | 2h | ⏳ Próximo |
| PostgreSQL | Média | 1.5h | ⏳ Próximo |
| Docker | Alta | 3h | ⏳ Próximo |
| Swagger | Média | 1h | ⏳ Próximo |
| CI/CD | Média | 1.5h | ⏳ Próximo |

---

## Como Contribuir

1. Escolher uma tarefa do roadmap
2. Criar branch: `git checkout -b feature/nome-da-feature`
3. Implementar a feature
4. Rodar testes: `python manage.py test`
5. Fazer commit: `git commit -m "feat: descrição"`
6. Fazer push e criar PR

---

## Dependências Instaladas

```
django==6.0.1
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.2
django-cors-headers==4.3.1
python-dotenv==1.0.0 (para produção)
psycopg2-binary==2.9.9 (para PostgreSQL)
drf-spectacular==0.26.5 (para Swagger)
sentry-sdk==1.40.1 (para monitoramento)
```

---

## Contato e Dúvidas

Para dúvidas sobre a implementação, consulte:
- README.md - Documentação geral
- Código comentado em `usuarios/views.py`
- Testes em `usuarios/tests.py`
