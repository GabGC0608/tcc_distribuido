# API

## Auth
- POST `/api/auth/register/`
- POST `/api/auth/login/` -> access/refresh JWT
- POST `/api/auth/refresh/`
- GET `/api/auth/me/`
- GET `/api/auth/audit/` (admin/coordenador)

## Monografias
- CRUD `/api/monographs/`
- POST `/api/monographs/{id}/approve/` (orientador)
- POST `/api/monographs/{id}/submit/`
- POST `/api/monographs/{id}/revoke-approval/`
- GET `/api/students/`, `/api/professors/`, `/api/courses/`

Upload: campo multipart `file`, somente PDF, máximo 50 MB. SHA-256 é calculado no servidor.

## Bancas
- CRUD `/api/defenses/`
- POST `/api/defenses/{id}/members/`
- POST `/api/defenses/{id}/members/{member_id}/availability/`
- POST `/api/defenses/{id}/evaluations/`
- POST `/api/defenses/{id}/close/`
- GET `/api/defenses/{id}/external-access/{token}/`

## Repositório público
- GET `/api/repository/monographs`
- GET `/api/repository/monographs/{id}`
- GET `/api/repository/monographs/{id}/download`
- filtros: `search`, `author`, `advisor`, `course`, `year`, `keyword`

## Relatórios
- GET `/api/reports/overview`
- GET `/api/reports/by-course`
- GET `/api/reports/by-advisor`
- GET `/api/reports/by-year`
