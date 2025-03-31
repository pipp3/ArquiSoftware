# Sistema de Gestión de Clínica Médica

Este proyecto implementa un sistema de gestión para una clínica médica utilizando una arquitectura orientada a servicios (SOA). El sistema está diseñado para manejar diferentes aspectos de la gestión médica, incluyendo citas, historiales médicos, notificaciones y más.

## 🏗️ Arquitectura

El sistema está construido utilizando una arquitectura orientada a servicios (SOA) con los siguientes componentes principales:

### Servicios Core
- **Base de Datos**: PostgreSQL 14.10
- **Bus de Servicios**: SOA Bus para comunicación entre servicios
- **Panel de Administración**: PgAdmin para gestión de base de datos

### Microservicios
1. **Servicio de Conexión a Base de Datos** (`dbcon-service`)
2. **Servicio de Autenticación** (`usrlg-service`)
3. **Servicio de Gestión de Usuarios** (`usrmn-service`)
4. **Servicio de Comentarios** (`comment-service`)
5. **Servicio de Historial Médico** (`history-service`)
6. **Servicio de Notificaciones** (`notification-service`)
7. **Servicio de Agendamiento** (`schedule-service`)
8. **Servicio de Cancelación** (`cancel-service`)
9. **Servicio de Reagendamiento** (`reschedule-service`)
10. **Servicio de Recetas** (`recipes-service`)

## 🚀 Requisitos Previos

- Docker
- Docker Compose
- Python 3.x

## 🔧 Configuración

1. Clonar el repositorio
2. Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```
   POSTGRES_USER=tu_usuario
   POSTGRES_DB=clinicaUDP
   POSTGRES_PASSWORD=tu_contraseña
   HIDE_EMPTY_PASSWORD=no
   TWILIO_ACCOUNT_SID=tu_sid
   TWILIO_AUTH_TOKEN=tu_token
   ```

## 🏃‍♂️ Ejecución

Para iniciar el sistema completo:

```bash
docker-compose up -d
```

Esto iniciará todos los servicios necesarios en contenedores Docker.

## 📊 Acceso a Servicios

- **Base de Datos PostgreSQL**: localhost:5432
- **PgAdmin**: http://localhost:8080
   - Email: admin@admin.com
   - Contraseña: admin
- **Bus de Servicios**: localhost:5000

## 📁 Estructura del Proyecto

```
.
├── customers/           # Clientes de prueba
├── db/                 # Scripts de inicialización de base de datos
├── services/           # Microservicios
├── docker-compose.yml  # Configuración de Docker Compose
└── .env               # Variables de entorno
```

## 🔄 Flujo de Trabajo

1. Los clientes se conectan al sistema a través de los servicios expuestos
2. Las solicitudes son procesadas por el bus de servicios
3. Los microservicios correspondientes manejan la lógica de negocio
4. Los datos son persistidos en la base de datos PostgreSQL
5. Las notificaciones son manejadas por el servicio de notificaciones

## 🛠️ Tecnologías Utilizadas

- Python
- PostgreSQL
- Docker
- Docker Compose
- SOABus
- Twilio (para notificaciones)

## 📝 Notas Adicionales

- Todos los servicios están configurados para reiniciarse automáticamente en caso de fallos
- La base de datos persiste sus datos en un volumen Docker
- Los servicios están conectados a través de una red Docker dedicada (`soanet`)

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles. 