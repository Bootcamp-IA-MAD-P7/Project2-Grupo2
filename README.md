# Project-CRUD-Python-G2
## 🧪 Cobertura de Calidad y Testing

El backend de **Iron Pulse** cuenta con una capa de pruebas automatizadas que garantizan la estabilidad del software y previenen regresiones en entornos de producción. Las pruebas se dividen en dos enfoques estratégicos:

### 1. Pruebas de Integración (Endpoints API)
Utilizando `TestClient` de FastAPI, se simulan peticiones HTTP reales para verificar el comportamiento de los controladores, el enrutamiento y la consistencia de las respuestas de la base de datos:
* **Gestión de Miembros (`test_member.py`):** Validación del flujo de registro (HTTP 201), control de excepciones por correos duplicados (HTTP 409) y consultas de perfiles existentes (HTTP 200).
* **Planes de Suscripción (`test_plan.py`):** Verificación de la persistencia de nuevas tarifas y captura controlada de errores en solicitudes de planes inexistentes (HTTP 404).
* **Transacciones Financieras (`test_payment.py`):** Automatización de auditorías de cobros vinculados directamente al identificador único del socio.

### 2. Pruebas Unitarias Aisladas (Capa de Servicios)
Para testear la lógica algorítmica de negocio de manera pura y sin dependencias de infraestructura, se utiliza `unittest.mock` (`MagicMock`), aislando por completo el acceso a la base de datos física:
* **Servicio de Socios (`test_member_service.py`):** Pruebas funcionales sobre las reglas de negocio de altas, bajas y penalizaciones.
* **Servicio de Accesos (`test_attendance_service.py`):** Verificación del motor de validación de entradas que cruza los datos de asistencia con la vigencia del plan de suscripción del socio.
* **Servicio de Analítica (`test_report_service.py`):** Pruebas de carga lógica sobre las funciones encargadas de procesar estadísticas agregadas financieras y de aforo.

---

## 🗺️ Documentación de la API (Endpoints del MVP)

A continuación se detallan las rutas principales integradas en la rama `developer` correspondientes al módulo de socios y tarifas:

### 👥 Módulo de Miembros (`/api/v1/members`)
* **`POST /` - Registrar Miembro:** Crea un nuevo perfil de socio en el sistema.
* **`GET /{member_id}` - Obtener Perfil:** Recupera los datos detallados de un socio específico mediante su ID único.

### 💳 Módulo de Planes de Suscripción (`/api/v1/plans`)
* **`POST /` - Crear Plan:** Da de alta una nueva modalidad de tarifa en el catálogo del gimnasio.
* **`GET /` - Listar Planes:** Devuelve el catálogo completo de suscripciones activas disponibles.

### 💰 Módulo de Pagos y Caja (`/api/v1/payments`)
* **`POST /` - Registrar Transacción:** Vincula un cobro exitoso a un miembro del gimnasio para activar o renovar su suscripción.


## Attendance, Reports and CSV Export Module

This module manages member attendance records linked to reservations. It allows the system to register when a member checks in for a reservation, optionally register a check-out time, list attendance records, generate attendance reports, and export attendance data to CSV.

### Main features

- Register member attendance for an existing reservation.
- Validate that the member exists and is active.
- Validate that the reservation exists.
- Validate that the reservation belongs to the selected member.
- Allow attendance only for confirmed reservations.
- Prevent duplicated attendance records for the same member and reservation.
- Register check-out time for attendance records.
- List attendances with pagination.
- Export attendances to CSV with optional filters.
- Generate attendance and income reports.

### Attendance endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/attendances/` | Registers a new attendance/check-in. |
| `GET` | `/api/v1/attendances/` | Lists attendances with pagination. |
| `GET` | `/api/v1/attendances/{attendance_id}` | Returns one attendance record by ID. |
| `POST` | `/api/v1/attendances/{attendance_id}/check-out` | Registers the check-out time for an attendance. |
| `GET` | `/api/v1/attendances/export-csv` | Exports attendances to CSV. |

### Attendance request example

```json
{
  "member_id": 1,
  "reservation_id": 1
}
```

### Attendance response example

```json
{
  "id": 1,
  "member_id": 1,
  "reservation_id": 1,
  "check_in": "2026-05-29T10:30:00Z",
  "check_out": null
}
```

### Attendance listing with pagination

The attendance listing endpoint supports pagination using `offset` and `limit`.

Example:

```http
GET /api/v1/attendances/?offset=0&limit=20
```

- `offset`: number of records to skip.
- `limit`: maximum number of records to return. Default value: `20`.

### CSV export

The CSV export endpoint returns attendance records as a downloadable `.csv` file.

```http
GET /api/v1/attendances/export-csv
```

Optional filters:

| Query param | Type | Description |
|---|---|---|
| `start_date` | `date` | Filters attendances from this date. |
| `end_date` | `date` | Filters attendances until this date. |
| `member_id` | `int` | Filters attendances by member. |
| `reservation_id` | `int` | Filters attendances by reservation. |

Example:

```http
GET /api/v1/attendances/export-csv?start_date=2026-05-01&end_date=2026-05-31&member_id=1
```

The CSV includes:

```text
id, member_id, reservation_id, check_in, check_out
```

### Report endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/reports/attendance` | Returns an attendance summary for a date range. |
| `GET` | `/api/v1/reports/attendance/by-member` | Groups attendances by member. |
| `GET` | `/api/v1/reports/attendance/by-reservation` | Groups attendances by reservation. |
| `GET` | `/api/v1/reports/attendance/by-shift` | Groups attendances by shift/class. |
| `GET` | `/api/v1/reports/income` | Returns completed payment income for a date range. |

### Report date filters

All report endpoints accept optional date range filters:

```http
GET /api/v1/reports/attendance?start_date=2026-05-01&end_date=2026-05-31
```

If no dates are provided, the report uses the current date by default.

### Attendance business rules

The attendance registration service applies the following validations:

- The member must exist.
- The member must be active.
- The reservation must exist.
- The reservation must belong to the member.
- The reservation must have status `confirmed`.
- A member cannot have duplicated attendance for the same reservation.
- Check-out can only be registered once.

### Related files

```text
app/models/attendance.py
app/schemas/attendance.py
app/services/attendance_service.py
app/services/attendance_export_service.py
app/routers/attendance.py
app/schemas/report.py
app/services/report_service.py
app/routers/report.py
app/tests/test_attendance.py
app/tests/test_report.py
app/scripts/seed_attendance_data.py
```

### Testing

Attendance tests cover:

- Successful attendance registration.
- Member not found.
- Reservation not found.
- Reservation not belonging to the member.
- Cancelled reservation validation.
- Duplicate attendance validation.
- Attendance listing with pagination.
- Attendance detail by ID.
- Check-out registration.
- Duplicate check-out validation.

Run tests with:

```bash
pytest app/tests/test_attendance.py
pytest app/tests/test_report.py
```

### Pending validation

The module requires final validation with:

- PostgreSQL running.
- Database tables created through Alembic or SQLModel metadata.
- Attendance and report routers registered in `main.py`.
- Real `Member` and `Reservation` data available.
- Functional testing from Swagger at `/api/docs`.


## 📋 Gestión del Negocio: Módulo de Planes y Estados

### 1. Modelado de Planes de Suscripción
En base a la estructura del archivo `plan.py`, el catálogo de tarifas del gimnasio se organiza bajo los siguientes parámetros del negocio:
* **Nombre del Plan (`name`):** Identificador único de la tarifa (ej. Plan Básico, Plan Premium).
* **Precio (`price`):** Valor numérico decimal que representa el coste mensual de la suscripción.
* **Duración (`duration_days`):** Período de validez del plan, configurado de manera predeterminada en 30 días.

### 2. Control de Estados del Miembro (MemberStatus)
Para garantizar la lógica de accesos en el backend, la enumeración de estados en `member.py` restringe los flujos a tres situaciones comerciales válidas:
* **Active:** Socio al corriente de pago con acceso total a las instalaciones y reservas.
* **Inactive:** Socio en situación de baja temporal o con la suscripción web caducada.
* **Suspended:** Acceso bloqueado por impagos del plan o por incidencias en el control de aforo.
