# DISEÑO DE BASE DE DATOS — SISTEMA DE GESTIÓN DE EVENTOS

## Diagrama Entidad-Relación

```mermaid
erDiagram
    User ||--o{ Event : organizes
    Event ||--o{ Invitation : contains
    Invitation ||--o| Attendance : records
    Event ||--o{ Attendance : tracks

    User {
        int id PK
        string email UK "Correo electrónico único"
        string username UK "Nombre de usuario único"
        string first_name "Nombres"
        string last_name "Apellidos"
        string phone NULL "Teléfono"
        string password_hash "Hash bcrypt/argon2"
        string profile_image NULL "Ruta imagen perfil"
        enum role "admin | organizer | collaborator"
        bool is_active "Cuenta activa?"
        bool is_staff "Acceso admin?"
        bool is_superuser "Superusuario?"
        datetime created_at "Fecha registro"
        datetime updated_at "Fecha actualización"
    }

    Event {
        int id PK
        string title "Título del evento"
        text description NULL "Descripción"
        date event_date "Fecha del evento"
        time event_time NULL "Hora del evento"
        string location NULL "Ubicación"
        enum category "conference | workshop | seminar | networking | social | corporate | other"
        string image NULL "Imagen del evento"
        enum status "draft | active | finished"
        int organizer_id FK "Usuario organizador"
        datetime created_at "Fecha creación"
        datetime updated_at "Fecha actualización"
    }

    Invitation {
        int id PK
        string first_name "Nombres invitado"
        string last_name "Apellidos invitado"
        string email "Email invitado"
        string phone NULL "Teléfono invitado"
        enum rsvp_status "pending | confirmed | rejected"
        int event_id FK "Evento asociado"
        datetime created_at "Fecha invitación"
        datetime updated_at "Fecha actualización"
    }

    Attendance {
        int id PK
        int invitation_id FK UK "Invitación (1:1)"
        int event_id FK "Evento"
        string qr_code UK "Hash único del QR"
        datetime checkin_time "Fecha/hora ingreso"
    }
```

## Modelo Relacional (SQL DDL)

```sql
-- ============================================================
-- TABLA: User (usuario personalizado)
-- ============================================================
CREATE TABLE "users_user" (
    "id"                INTEGER       NOT NULL PRIMARY KEY AUTOINCREMENT,
    "password"          VARCHAR(128)  NOT NULL,
    "last_login"        DATETIME      NULL,
    "is_superuser"      BOOLEAN       NOT NULL,
    "email"             VARCHAR(254)  NOT NULL UNIQUE,
    "username"          VARCHAR(150)  NOT NULL UNIQUE,
    "first_name"        VARCHAR(150)  NOT NULL,
    "last_name"         VARCHAR(150)  NOT NULL,
    "phone"             VARCHAR(20)   NULL,
    "profile_image"     VARCHAR(100)  NULL,
    "role"              VARCHAR(20)   NOT NULL DEFAULT 'organizer',
    "is_active"         BOOLEAN       NOT NULL DEFAULT 1,
    "is_staff"          BOOLEAN       NOT NULL DEFAULT 0,
    "created_at"        DATETIME      NOT NULL,
    "updated_at"        DATETIME      NOT NULL
);

CREATE INDEX "idx_user_email"    ON "users_user" ("email");
CREATE INDEX "idx_user_username" ON "users_user" ("username");
CREATE INDEX "idx_user_role"     ON "users_user" ("role");

-- ============================================================
-- TABLA: Event
-- ============================================================
CREATE TABLE "events_event" (
    "id"                INTEGER       NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title"             VARCHAR(200)  NOT NULL,
    "description"       TEXT          NULL,
    "event_date"        DATE          NOT NULL,
    "event_time"        TIME          NULL,
    "location"          VARCHAR(255)  NULL,
    "category"          VARCHAR(100)  NOT NULL DEFAULT 'other',
    "image"             VARCHAR(100)  NULL,
    "status"            VARCHAR(20)   NOT NULL DEFAULT 'draft',
    "organizer_id"      BIGINT        NOT NULL REFERENCES "users_user" ("id"),
    "created_at"        DATETIME      NOT NULL,
    "updated_at"        DATETIME      NOT NULL
);

CREATE INDEX "idx_event_date"     ON "events_event" ("event_date");
CREATE INDEX "idx_event_status"   ON "events_event" ("status");
CREATE INDEX "idx_event_category" ON "events_event" ("category");
CREATE INDEX "idx_event_organizer" ON "events_event" ("organizer_id");

-- ============================================================
-- TABLA: Invitation
-- ============================================================
CREATE TABLE "invitations_invitation" (
    "id"                INTEGER       NOT NULL PRIMARY KEY AUTOINCREMENT,
    "first_name"        VARCHAR(150)  NOT NULL,
    "last_name"         VARCHAR(150)  NOT NULL,
    "email"             VARCHAR(254)  NOT NULL,
    "phone"             VARCHAR(20)   NULL,
    "rsvp_status"       VARCHAR(20)   NOT NULL DEFAULT 'pending',
    "event_id"          BIGINT        NOT NULL REFERENCES "events_event" ("id"),
    "created_at"        DATETIME      NOT NULL,
    "updated_at"        DATETIME      NOT NULL,

    CONSTRAINT "uq_event_email" UNIQUE ("event_id", "email")
);

CREATE INDEX "idx_invitation_event" ON "invitations_invitation" ("event_id");
CREATE INDEX "idx_invitation_rsvp"  ON "invitations_invitation" ("rsvp_status");
CREATE INDEX "idx_invitation_email" ON "invitations_invitation" ("email");

-- ============================================================
-- TABLA: Attendance
-- ============================================================
CREATE TABLE "attendance_attendance" (
    "id"                INTEGER       NOT NULL PRIMARY KEY AUTOINCREMENT,
    "invitation_id"     BIGINT        NOT NULL UNIQUE REFERENCES "invitations_invitation" ("id"),
    "event_id"          BIGINT        NOT NULL REFERENCES "events_event" ("id"),
    "qr_code"           VARCHAR(255)  NOT NULL UNIQUE,
    "checkin_time"      DATETIME      NOT NULL
);

CREATE INDEX "idx_attendance_qr"      ON "attendance_attendance" ("qr_code");
CREATE INDEX "idx_attendance_event"   ON "attendance_attendance" ("event_id");
CREATE INDEX "idx_attendance_checkin" ON "attendance_attendance" ("checkin_time");
```

## Resumen de Tablas y Relaciones

### Tablas

| # | Tabla | Propósito | Filas estimadas |
|---|-------|-----------|-----------------|
| 1 | `users_user` | Usuarios del sistema con roles (admin, organizer, collaborator) | Bajo ~ centenas |
| 2 | `events_event` | Eventos creados por organizadores con ciclo de vida (draft → active → finished) | Medio ~ miles |
| 3 | `invitations_invitation` | Invitados por evento con estados RSVP | Alto ~ decenas de miles |
| 4 | `attendance_attendance` | Registro de check-in con QR único | Alto ~ decenas de miles |

### Relaciones

| Desde | Hacia | Tipo | Campo FK | Restricción |
|-------|-------|------|----------|-------------|
| `events_event` | `users_user` | N:1 | `organizer_id` | CASCADE al eliminar usuario |
| `invitations_invitation` | `events_event` | N:1 | `event_id` | CASCADE al eliminar evento |
| `attendance_attendance` | `invitations_invitation` | 1:1 | `invitation_id` (UNIQUE) | CASCADE al eliminar invitación |
| `attendance_attendance` | `events_event` | N:1 | `event_id` | CASCADE al eliminar evento |

### Restricciones Clave

1. **uq_event_email**: Un mismo email no puede ser invitado dos veces al mismo evento.
2. **UNIQUE(invitation_id) en Attendance**: Un invitado solo puede hacer check-in una vez.
3. **UNIQUE(qr_code) en Attendance**: Cada código QR es globalmente único.
4. **Transiciones de estado**: `draft → active → finished` (sin retroceso).

## Migración a PostgreSQL

Para cambiar a PostgreSQL en producción, solo se requiere:

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

No se requieren cambios en los modelos. Django ORM es agnóstico a la base de datos.
