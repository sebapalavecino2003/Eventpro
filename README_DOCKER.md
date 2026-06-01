# Docker para desarrollo local

## Requisitos

- Docker
- Docker Compose

## Construcción y ejecución

```bash
# Construir y levantar los servicios
docker compose up --build

# En segundo plano
docker compose up --build -d
```

## Acceso

| Servicio  | URL                          |
|-----------|------------------------------|
| Frontend  | http://localhost:5173        |
| Backend   | http://localhost:8000        |
| Admin     | http://localhost:8000/admin/ |

## Comandos útiles

### Ver logs

```bash
# Todos los servicios
docker compose logs -f

# Solo backend
docker compose logs -f backend

# Solo frontend
docker compose logs -f frontend
```

### Acceder a un contenedor

```bash
# Backend
docker compose exec backend bash

# Frontend
docker compose exec frontend sh
```

### Migraciones Django

```bash
docker compose exec backend python manage.py migrate
```

### Crear superusuario

```bash
docker compose exec backend python manage.py createsuperuser
```

### Recolectar archivos estáticos

```bash
docker compose exec backend python manage.py collectstatic --noinput
```

### Detener los servicios

```bash
docker compose down
```

### Detener y eliminar volúmenes (borra la BD)

```bash
docker compose down -v
```

## Persistencia de datos

La base de datos SQLite se almacena en `backend/db.sqlite3` y persiste aunque los contenedores se detengan. Se elimina solo si corres `docker compose down -v`.

## Hot reload

- **Frontend**: Vite recarga automáticamente al editar archivos en `frontend/`.
- **Backend**: Django runserver se reinicia automáticamente al editar archivos en `backend/`.

## Solución de errores comunes

### Puerto en uso

```bash
# Verificar qué proceso usa el puerto
sudo lsof -i :8000
sudo lsof -i :5173

# Usar un puerto diferente
# En docker-compose.yml: cambia "8000:8000" por "8001:8000"
```

### Permisos de la base de datos

```bash
# Si SQLite da error de permisos
docker compose exec backend chmod 664 db.sqlite3
```

### Reconstruir desde cero

```bash
docker compose down -v
docker compose up --build
```

### Errores de dependencias

```bash
# Reconstruir sin cache
docker compose build --no-cache
docker compose up
```
