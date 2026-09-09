# Sistema Distribuído de Monografias (TCC)

## Arquitetura

- `auth-service`: usuários, papéis, login/JWT e auditoria.
- `monograph-service`: alunos, professores, cursos, monografias, upload PDF, SHA-256 e aprovação do orientador.
- `defense-service`: bancas, membros, disponibilidade, avaliações e resultado.
- `repository-service`: catálogo público e busca full-text simples, alimentado por eventos.
- `notification-service`: consumidor de eventos e registro de notificações.
- `report-service`: métricas e dashboard JSON.
- PostgreSQL: banco separado por serviço.
- Redis: cache, rate limiting e controle de upload.
- RabbitMQ: eventos assíncronos.



## O sistema permite:

- Cadastro de alunos, professores e cursos;
- Cadastro e submissão de monografias;
- Upload e validação de arquivos PDF;
- Aprovação pelo orientador;
- Agendamento de bancas;
- Cadastro de membros da banca;
- Registro de avaliações;
- Publicação de monografias aprovadas;
- Pesquisa pública;
- Notificações;
- Relatórios e métricas.


## Requisitos do enunciado atendidos

Autenticação por login/senha, permissões por papel, auditoria, CRUD REST, upload somente PDF até 50 MB, SHA-256, aprovação obrigatória do orientador antes da banca, eventos assíncronos para extração/indexação/notificação, repositório público sem autenticação, Redis e RabbitMQ.

## Subir tudo

```bash
docker compose up --build
```

Serviços:
- Auth: http://localhost:8001
- Monografias: http://localhost:8002
- Bancas: http://localhost:8003
- Repositório: http://localhost:8004
- Notificações: http://localhost:8005
- Relatórios: http://localhost:8006

## Migrações

Os containers executam `makemigrations`/`migrate` no startup.

## Criar superusuário

```bash
docker compose exec auth-service python manage.py createsuperuser
```

## Teste rápido

```bash
curl http://localhost:8004/api/repository/monographs
curl http://localhost:8006/api/reports/overview
```

Consulte `docs/API.md` para os endpoints.

## Versões

O projeto foi fixado em Django 6.1.1, Django REST Framework 3.18.1 e django-allauth 65.19.2. Em 8/09/2026, Django 6.1 é a linha atual e o allauth 65.19.x declara suporte oficial a Django 6.1.
