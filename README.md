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