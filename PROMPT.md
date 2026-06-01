# PROYECTO: SISTEMA WEB DE GESTIÓN DE EVENTOS

Actúa como un arquitecto de software senior, analista funcional, diseñador de bases de datos, desarrollador backend Django y desarrollador frontend React con experiencia en sistemas empresariales.

Tu objetivo es diseñar y desarrollar una aplicación web completa para gestión de eventos orientada a empresas y emprendedores.

==================================================
TECNOLOGÍAS OBLIGATORIAS
==================================================

Frontend:
- React
- JSX
- JavaScript
- React Router
- Axios

Backend:
- Django
- Django REST Framework
- JWT Authentication

Base de Datos:
- SQLite

==================================================
REQUISITOS IMPORTANTES
==================================================

- NO utilizar el modelo User predeterminado de Django.
- Crear un modelo de usuario personalizado utilizando AbstractBaseUser y PermissionsMixin.
- Toda la autenticación debe funcionar sobre este usuario personalizado.
- Aplicar buenas prácticas de arquitectura y programación.
- Diseñar el sistema para que pueda migrarse fácilmente a PostgreSQL en el futuro.
- Utilizar API REST para toda la comunicación entre frontend y backend.
- Mantener una arquitectura limpia, escalable y mantenible.
- Separar responsabilidades en todo momento.

==================================================
OBJETIVO DEL SISTEMA
==================================================

El sistema permitirá a empresas y emprendedores organizar y gestionar eventos.

Los usuarios podrán:

- Crear una cuenta.
- Iniciar sesión.
- Administrar su perfil.
- Crear eventos.
- Modificar eventos.
- Eliminar eventos.
- Gestionar invitados.
- Confirmar asistencia.
- Realizar check-in mediante códigos QR.
- Consultar estadísticas de asistencia.

==================================================
FUNCIONALIDADES QUE NO DEBEN EXISTIR
==================================================

NO incluir:

- Venta de entradas.
- Pasarela de pagos.
- Mercado Pago.
- Stripe.
- Inteligencia Artificial.
- Chatbots.
- Recomendaciones automáticas.
- Predicciones.
- Generación automática de contenido.
- Automatizaciones basadas en IA.

==================================================
MÓDULO DE AUTENTICACIÓN
==================================================

Funcionalidades:

- Registro de usuarios.
- Inicio de sesión.
- Cierre de sesión.
- Recuperación de contraseña.
- Cambio de contraseña.
- Edición de perfil.
- Actualización de datos personales.

Modelo de usuario personalizado:

Campos mínimos:

- id
- email
- username
- first_name
- last_name
- phone
- profile_image
- role
- is_active
- is_staff
- created_at
- updated_at

Roles:

- Administrador
- Organizador
- Colaborador

==================================================
MÓDULO DE EVENTOS
==================================================

Cada evento debe contener:

- id
- nombre
- descripción
- fecha
- hora
- ubicación
- categoría
- imagen
- estado
- organizador
- fecha de creación
- fecha de actualización

Estados:

- Borrador
- Activo
- Finalizado

Funcionalidades:

- Crear evento
- Editar evento
- Eliminar evento
- Listar eventos
- Ver detalle del evento
- Cambiar estado

==================================================
MÓDULO DE INVITADOS
==================================================

Cada invitado debe contener:

- id
- nombre
- apellido
- email
- teléfono
- evento asociado
- estado RSVP

Estados RSVP:

- Pendiente
- Confirmado
- Rechazado

Funcionalidades:

- Agregar invitado
- Editar invitado
- Eliminar invitado
- Listar invitados
- Confirmar asistencia

==================================================
MÓDULO DE ASISTENCIA
==================================================

Funcionalidades:

- Generación de QR único por invitado
- Escaneo de QR
- Registro de ingreso
- Historial de asistencia

Campos:

- id
- invitado
- evento
- fecha_hora_ingreso
- qr_code

==================================================
MÓDULO DASHBOARD
==================================================

Mostrar:

- Total de eventos
- Próximos eventos
- Eventos finalizados
- Total de invitados
- Invitados confirmados
- Invitados pendientes
- Estadísticas básicas

==================================================
MÓDULO CALENDARIO
==================================================

Funcionalidades:

- Vista mensual
- Vista semanal
- Visualización de eventos programados

==================================================
ESTRUCTURA DEL FRONTEND
==================================================

La estructura debe ser simple y plana.

NO crear subcarpetas dentro de:

- pages
- components
- assets

Estructura obligatoria:

src/
├── assets/
│   ├── logo.png
│   ├── default-avatar.png
│   ├── banner.jpg
│   └── otros recursos

├── components/
│   ├── Navbar.jsx
│   ├── Sidebar.jsx
│   ├── EventCard.jsx
│   ├── GuestCard.jsx
│   ├── EventForm.jsx
│   ├── GuestForm.jsx
│   ├── Modal.jsx
│   ├── Loading.jsx
│   └── demás componentes

├── pages/
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Dashboard.jsx
│   ├── Events.jsx
│   ├── EventDetail.jsx
│   ├── Guests.jsx
│   ├── Calendar.jsx
│   ├── Profile.jsx
│   └── NotFound.jsx

├── styles/
│   ├── Login.css
│   ├── Register.css
│   ├── Dashboard.css
│   ├── Events.css
│   ├── EventDetail.css
│   ├── Guests.css
│   ├── Calendar.css
│   ├── Profile.css
│   ├── Navbar.css
│   ├── Sidebar.css
│   ├── EventCard.css
│   ├── GuestCard.css
│   ├── Modal.css
│   ├── variables.css
│   ├── reset.css
│   └── global.css

├── services/
├── hooks/
├── context/
├── routes/
├── utils/
├── constants/
├── validations/
├── layouts/
├── App.jsx
└── main.jsx

==================================================
REGLAS DEL FRONTEND
==================================================

- Separar completamente lógica y estilos.
- Cada página debe tener su CSS propio.
- Cada componente debe tener su CSS propio.
- No utilizar estilos inline.
- Utilizar variables CSS centralizadas.
- Crear rutas protegidas.
- Implementar manejo global de errores.
- Utilizar componentes reutilizables.

==================================================
ESTRUCTURA DEL BACKEND
==================================================

backend/
├── config/
├── apps/
│   ├── users/
│   ├── events/
│   ├── invitations/
│   ├── attendance/
│   └── dashboard/
│
├── media/
├── static/
├── logs/
├── requirements/
└── manage.py

==================================================
PARA CADA APP DJANGO GENERAR
==================================================

- models.py
- serializers.py
- views.py
- urls.py
- permissions.py
- services.py
- validators.py
- admin.py
- tests/

Explicar la responsabilidad de cada archivo.

==================================================
BASE DE DATOS
==================================================

Diseñar:

- Tablas
- Relaciones
- Claves foráneas
- Restricciones
- Índices

Generar:

- Diagrama Entidad Relación
- Modelo Relacional
- Explicación de tablas
- Explicación de relaciones

==================================================
API REST
==================================================

Diseñar completamente:

Autenticación:

POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
POST /api/auth/forgot-password
POST /api/auth/change-password

Usuarios:

GET /api/users/profile
PUT /api/users/profile

Eventos:

GET /api/events
POST /api/events
GET /api/events/{id}
PUT /api/events/{id}
DELETE /api/events/{id}

Invitados:

GET /api/invitations
POST /api/invitations
PUT /api/invitations/{id}
DELETE /api/invitations/{id}

Asistencia:

POST /api/attendance/checkin
GET /api/attendance

Dashboard:

GET /api/dashboard/stats

Para cada endpoint generar:

- Método HTTP
- Request
- Response
- Validaciones
- Permisos
- Código de estado

==================================================
SEGURIDAD
==================================================

Implementar:

- JWT Authentication
- Permisos por rol
- Validación de datos
- Protección de endpoints
- Protección de rutas frontend
- Manejo de errores
- Buenas prácticas OWASP

==================================================
DIAGRAMAS UML
==================================================

Generar:

1. Casos de uso
2. Diagrama de clases
3. Diagrama de secuencia
4. Diagrama de componentes

==================================================
HISTORIAS DE USUARIO
==================================================

Generar historias de usuario completas.

Formato:

Como [rol]
Quiero [acción]
Para [beneficio]

==================================================
CASOS DE USO
==================================================

Generar casos de uso detallados para cada módulo.

==================================================
ROADMAP
==================================================

Generar:

- Roadmap completo
- Orden recomendado de desarrollo
- Dependencias entre módulos
- Estimación de complejidad
- Prioridades

==================================================
RESULTADO ESPERADO
==================================================

Quiero una documentación técnica profesional, extremadamente detallada y lista para servir como guía de desarrollo del proyecto.

Explicar y justificar todas las decisiones arquitectónicas.

No omitir detalles técnicos.

Generar la solución como si fuera un proyecto universitario de Ingeniería en Computación preparado para ser defendido ante docentes y evaluadores.
