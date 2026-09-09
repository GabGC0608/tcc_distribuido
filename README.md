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

## Subir tudo (Docker — recomendado só para teste/desenvolvimento rápido)

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

## Rodar nativamente (sem Docker)

O projeto não depende de Docker: cada serviço é um projeto Django comum. Requisitos
locais: Python 3.13, PostgreSQL, Redis e RabbitMQ instalados/rodando na máquina (ou
apontando via variáveis de ambiente para instâncias já existentes).

Para cada serviço em `services/<nome>-service`:

```bash
cd services/auth-service   # repita para cada serviço
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../../.env.example .env   # ajuste DB_NAME, DB_USER, DB_PASSWORD etc.
python manage.py migrate
python manage.py runserver 0.0.0.0:8001   # porta de cada serviço, ver tabela acima
```

Os defaults de `DB_HOST` e `RABBITMQ_URL` já apontam para `localhost`; ao rodar via
`docker compose`, o próprio compose sobrescreve essas variáveis para os hostnames dos
containers (`postgres`, `rabbitmq`), então os dois modos convivem sem conflito.

Cada serviço precisa de um banco PostgreSQL próprio (ex.: `tcc_auth`, `tcc_monograph`,
...) — crie-os localmente com o mesmo usuário/senha do `.env`.

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

# 1. Tecnologias utilizadas

- Python 3.13
- Django
- Django REST Framework
- PostgreSQL
- Redis
- RabbitMQ
- Docker
- Docker Compose
- JWT
- PyPDF2

---

# 2. Arquitetura do sistema

```text
                         USUÁRIO
                            │
                            ▼
                    ┌────────────────┐
                    │ Frontend / API │
                    └───────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │    AUTH    │ │ MONOGRAPH  │ │  DEFENSE   │
       │   :8001    │ │   :8002    │ │   :8003    │
       └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   RabbitMQ    │
                    │  Mensageria   │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │ REPOSITORY │ │NOTIFICATION│ │   REPORT   │
       │   :8004    │ │   :8005    │ │   :8006    │
       └─────┬──────┘ └────────────┘ └────────────┘
             │
             ▼
       ┌──────────────┐
       │ PostgreSQL   │
       └──────────────┘

              ┌──────────────┐
              │    Redis     │
              │ Cache / apoio│
              └──────────────┘

## Versões

O projeto foi fixado em Django 6.1.1, Django REST Framework 3.18.1 e django-allauth 65.19.2. Em 8/09/2026, Django 6.1 é a linha atual e o allauth 65.19.x declara suporte oficial a Django 6.1.
