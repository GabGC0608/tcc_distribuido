# SPEC — Sistema Distribuído de Monografias (TCC)

> Baseado no enunciado do trabalho de Sistemas Distribuídos (Prof. Alessandro Vivas Andrade).
> Fonte original: `Trabalho_SistemasDistribuidos_Monografias (1).md`.

## 1. Objetivo

Implementar um sistema distribuído para cadastro, submissão, avaliação e publicação de
monografias (TCC), permitindo que:

- alunos submetam seus trabalhos;
- orientadores acompanhem e aprovem a submissão;
- coordenadores agendem bancas de defesa;
- o público em geral pesquise monografias aprovadas em um repositório digital.

Regras centrais:

- submissão para banca só ocorre após aprovação do orientador;
- upload valida formato, tamanho e hash criptográfico (SHA-256);
- publicação no repositório público é automática, e só ocorre após aprovação em defesa
  e assinatura do termo de autorização de publicação;
- o sistema deve suportar milhares de acessos simultâneos ao repositório público
  (cache Redis, filas de eventos, microsserviços).

## 2. Stack obrigatória

- Python + Django (última versão) + Django REST Framework
- PostgreSQL (um banco por serviço)
- Redis (cache, controle de submissões, rate limiting)
- RabbitMQ ou Kafka (fila de eventos)
- Biblioteca de extração de texto de PDF (PyPDF2 / pdfplumber)
- Frontend em JavaScript, consumindo a API
- django-allauth para autenticação
- Grupos de até 5 alunos, ambiente Linux

## 3. Arquitetura de microsserviços

| Serviço | Porta | Responsabilidade |
|---|---|---|
| `auth-service` | 8001 | login/JWT, usuários, papéis, permissões, auditoria |
| `monograph-service` | 8002 | alunos, professores, cursos, monografias, upload PDF, hash SHA-256, aprovação do orientador |
| `defense-service` | 8003 | bancas, membros, disponibilidade, avaliações, resultado final |
| `repository-service` | 8004 | catálogo público, busca full-text, indexação via eventos |
| `notification-service` | 8005 | consumo de eventos, envio de notificações/e-mails |
| `report-service` | 8006 | métricas, dashboard |

Infra compartilhada: PostgreSQL (um schema/DB por serviço), Redis, RabbitMQ — todos
orquestrados via `docker-compose.yml`.

## 4. Modelos principais

- **Usuário / Papel**: administrador, coordenador, professor/orientador, aluno,
  membro de banca externo (token temporário, sem conta permanente)
- **Aluno**: nome, matrícula, email, curso, orientador atual
- **Professor**: nome, email, departamento, área de pesquisa
- **Curso**: nome, código, coordenador
- **Monografia**: título, resumo, palavras-chave, aluno, orientador, curso, data de
  submissão, arquivo (PDF), hash SHA-256, status (rascunho / em avaliação / aprovada /
  reprovada / publicada)
- **Banca**: monografia, data, local/link, membros, status (agendada / realizada / cancelada)
- **Avaliação**: banca, membro avaliador, nota, parecer, recomendação
- **Documento Complementar**: monografia, tipo (ata de defesa, termo de autorização,
  comprovante de correção), arquivo
- **Log de Auditoria**: quem, o quê, quando (para todo o histórico de alterações)

## 5. Fluxos principais

### 5.1 Autenticação
- Login/senha com django-allauth, senhas criptografadas, política de senha forte.
- Controle de acesso por papel (admin, coordenador, professor, aluno, membro externo por token).
- Auditoria de ações. Dashboard personalizado por tipo de usuário.

### 5.2 Submissão de monografia
1. Aluno cria rascunho e associa orientador.
2. Aluno faz upload do PDF (≤ 50 MB, somente PDF).
3. Servidor calcula SHA-256 (dedup + integridade).
4. Extração de texto do PDF ocorre **assíncrona**, via fila de eventos (não bloqueia o upload).
5. Orientador aprova/reprova. Só após aprovação a monografia pode ir a banca.

### 5.3 Agendamento de banca
1. Coordenador/orientador agenda banca para monografia já aprovada pelo orientador.
2. Define data, local ou link, convida membros (inclui externos via token temporário).
3. Sistema valida: aprovação prévia, disponibilidade confirmada de todos os membros,
   ausência de conflito de horário.
4. Notificação assíncrona (fila de eventos) a membros e aluno.
5. Após a defesa, cada membro registra avaliação (nota + parecer).
6. Resultado final só é calculado quando todas as avaliações estiverem registradas.

### 5.4 Publicação no repositório
1. Aprovação final em banca + versão corrigida (se houver ressalvas) + termo de
   autorização assinado ⇒ publicação automática.
2. Repositório público pesquisável por título, autor, orientador, curso, ano, palavras-chave.
3. Leitura pública não exige autenticação; escrita/administração exige autenticação e
   (para área administrativa) validação de rede institucional (IP/VPN).

### 5.5 CRUD
CRUD completo para alunos, professores, cursos, monografias, bancas, avaliações, com
regras de quem pode criar/editar/excluir (nunca excluir monografia já publicada).

## 6. API REST

### Públicos
- `GET /api/repository/monographs` (busca e filtros)
- `GET /api/courses/`
- `GET /api/professors/` (orientadores)

### Restritos (autenticados)
- CRUD `/api/students/`, `/api/monographs/`, `/api/defenses/`, avaliações
- Exemplos: `POST /api/monographs/`, `POST /api/defenses/`,
  `GET /api/repository/monographs?search=sistemas+distribuidos`

Ver detalhamento real implementado em `docs/API.md`.

## 7. Redis

- cache de sessões
- cache de resultados de busca (`busca:hash_da_query`)
- controle de upload em processamento (`upload_em_andamento:monografia_id`)
- rate limiting de submissões

## 8. Fila de eventos

Eventos: submissão de monografia, agendamento de banca, avaliação registrada, publicação.
Fluxo exemplo: *aluno submete → evento na fila → extração/indexação de texto →
notificação ao orientador.*

## 9. Dashboard

Gráficos (Chart.js ou Plotly):
- monografias por curso
- monografias por orientador
- monografias por ano de defesa
- taxa de aprovação
- tempo médio entre submissão e defesa

## 10. Frontend

Interface web em JavaScript, consumindo a API, cobrindo:
- submissão de monografia (aluno)
- aprovação (orientador)
- agendamento de banca (coordenador)
- lançamento de avaliação (membros de banca)
- pesquisa pública no repositório

## 11. Histórico de alterações

Registrar, para toda alteração relevante: quem fez, o que mudou, data/hora.

## 12. Estado atual do projeto (2026-09-09)

Já implementado (scaffolding Django completo, containers subindo):
- Os 6 microsserviços (`auth`, `monograph`, `defense`, `repository`, `notification`, `report`)
  com models, serializers, views, permissions, tasks e workers.
- `docker-compose.yml` com Postgres por serviço, Redis e RabbitMQ.
- API documentada em `docs/API.md` (auth, monografias, bancas, repositório, relatórios).

Pendente / a validar (vira backlog):
- Frontend em JavaScript (não existe ainda no repo).
- Dashboard com gráficos (Chart.js/Plotly).
- Confirmar cobertura de auditoria em todos os serviços (hoje só há sinais em `auth-service`
  e `monograph-service`).
- Testes automatizados end-to-end dos fluxos críticos (aprovação → banca → avaliação → publicação).
- Validação de acesso por rede institucional (IP/VPN) na área administrativa.
- Acesso temporário de membros de banca externos via token.
- Revisão de regras de exclusão (nunca excluir monografia publicada).
