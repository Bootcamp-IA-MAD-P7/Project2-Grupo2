# Project-CRUD-Python-G2


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