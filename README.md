# API Odoo (SendTrack)


## Swagger UI
Swagger:
`http://localhost:8069/api/docs`


## Arranque

Levantar contenedores:

```bash
docker compose up -d
```

Credenciales admin en `http://localhost:8069`:
- User: `admin`
- Password: `admin`


## Endpoints

### Auth

#### Register
`POST /api/auth/register`

Body:
```json
{
  "name": "Pepe",
  "email": "pepe@test.com",
  "password": "1234password",
  "phone": "600123456",
  "street": "Calle Mayor 12"
}
```

Respuesta:
```json
{
  "user_id": 7,
  "partner_id": 9,
  "name": "Pepe",
  "email": "pepe@test.com",
  "phone": "600123456",
  "street": "Calle Mayor 12"
}
```

#### Login
`POST /api/auth/login`

Body:
```json
{
  "email": "pepe@test.com",
  "password": "1234password"
}
```

Respuesta:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 7,
  "partner_id": 9,
  "name": "Pepe",
  "email": "pepe@test.com",
  "phone": "600123456",
  "street": "Calle Mayor 12"
}
```

#### Logout
`POST /api/auth/logout`

Body: `{}`

Respuesta:
```json
{
  "status": "logged_out"
}
```

---

### Envíos

#### Crear envío
`POST /api/shipments`

Body:
```json
{
  "sender_id": 3,
  "receiver_name": "Ana Lopez",
  "receiver_email": "ana@test.com",
  "receiver_phone": "611223344",
  "delivery_address": "Av Diagonal 100",
  "weight": 1.5,
  "notes": "Piso 2"
}
```

Respuesta:
```json
{
  "id": 1,
  "name": "SHP-A1B2C3D4",
  "tracking_code": "E5F6G7H8I9J0",
  "sender_id": 3,
  "sender_name": "Pepe",
  "sender_email": "pepe@test.com",
  "sender_phone": "600123456",
  "receiver_id": 4,
  "receiver_name": "Ana Lopez",
  "receiver_email": "ana@test.com",
  "receiver_phone": "611223344",
  "delivery_address": "Av Diagonal 100",
  "weight": 1.5,
  "status": "draft",
  "notes": "Piso 2",
  "created_at": "2026-10-12 18:00:00"
}
```

#### Listar envíos de una persona
`GET /api/shipments/person/<partner_id>`

Filtro opcional con query param: `?role=sender` o `?role=receiver`

Respuesta:
```json
[
  {
    "id": 1,
    "name": "SHP-A1B2C3D4",
    "tracking_code": "E5F6G7H8I9J0",
    "sender_id": 3,
    "sender_name": "Pepe",
    "sender_email": "pepe@test.com",
    "sender_phone": "600123456",
    "receiver_id": 4,
    "receiver_name": "Ana Lopez",
    "receiver_email": "ana@test.com",
    "receiver_phone": "611223344",
    "delivery_address": "Av Diagonal 100",
    "weight": 1.5,
    "status": "draft",
    "notes": "Piso 2",
    "created_at": "2026-10-12 18:00:00"
  }
]
```

#### Tracking de un envío
`GET /api/shipments/track/<tracking_code>`

Respuesta:
```json
{
  "id": 1,
  "name": "SHP-A1B2C3D4",
  "tracking_code": "E5F6G7H8I9J0",
  "sender_id": 3,
  "sender_name": "Pepe",
  "sender_email": "pepe@test.com",
  "sender_phone": "600123456",
  "receiver_id": 4,
  "receiver_name": "Ana Lopez",
  "receiver_email": "ana@test.com",
  "receiver_phone": "611223344",
  "delivery_address": "Av Diagonal 100",
  "weight": 1.5,
  "status": "draft",
  "notes": "Piso 2",
  "created_at": "2026-10-12 18:00:00"
}
```

---

### Tickets

#### Crear ticket
`POST /api/tickets`

Body:
```json
{
  "title": "Paquete golpeado",
  "description": "Ha llegado la caja rota",
  "partner_id": 3,
  "tracking_code": "E5F6G7H8I9J0",
  "priority": "high"
}
```

Respuesta:
```json
{
  "id": 1,
  "name": "TCK-9A8B7C6D",
  "title": "Paquete golpeado",
  "description": "Ha llegado la caja rota",
  "partner_id": 3,
  "partner_name": "Pepe",
  "partner_email": "pepe@test.com",
  "shipment_id": 1,
  "shipment_tracking_code": "E5F6G7H8I9J0",
  "priority": "high",
  "status": "open",
  "created_at": "2026-10-12 18:05:00"
}
```

#### Listar tickets de una persona
`GET /api/tickets/person/<partner_id>`

Respuesta:
```json
[
  {
    "id": 1,
    "name": "TCK-9A8B7C6D",
    "title": "Paquete golpeado",
    "description": "Ha llegado la caja rota",
    "partner_id": 3,
    "partner_name": "Pepe",
    "partner_email": "pepe@test.com",
    "shipment_id": 1,
    "shipment_tracking_code": "E5F6G7H8I9J0",
    "priority": "high",
    "status": "open",
    "created_at": "2026-10-12 18:05:00"
  }
]
```
