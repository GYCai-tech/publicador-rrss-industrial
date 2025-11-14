# 🏭 Publicador Industrial - Sistema de Gestión de Contenido

Sistema automatizado para gestión y publicación de contenido en múltiples plataformas sociales y de comunicación.

## 🚀 Características

- ✅ Generación de contenido con IA para múltiples plataformas
- ✅ Programación automática de publicaciones
- ✅ Gestión de contactos y listas de distribución
- ✅ Historial completo de publicaciones enviadas
- ✅ Calendario visual de publicaciones programadas
- ✅ Soporte para LinkedIn, Instagram, WordPress, Gmail y WhatsApp

## 🔧 Instalación

### Prerrequisitos
- Docker y Docker Compose instalados
- Credenciales de API para las plataformas que desees usar

### Configuración

1. Clona el repositorio:
```bash
git clone https://github.com/GYCai-tech/publicador-industrial.git
cd publicador-industrial
```

2. Copia el archivo de ejemplo y configura tus variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus credenciales
```

3. Construye y levanta los contenedores:
```bash
docker-compose up -d --build
```

4. Accede a la aplicación en: http://localhost:8504

## 📁 Estructura de Directorios

- `data-industrial/` - Base de datos SQLite
- `media-industrial/` - Archivos multimedia
- `output-industrial/` - Salidas generadas
- `temp-industrial/` - Archivos temporales
- `sessions-industrial/` - Sesiones de autenticación

## 🔐 Variables de Entorno

Configura las siguientes variables en tu archivo `.env`:

```env
# OpenAI
OPENAI_API_KEY=tu_api_key

# Instagram (opcional)
INSTAGRAM_USERNAME=tu_usuario
INSTAGRAM_PASSWORD=tu_password

# LinkedIn (opcional)
LINKEDIN_CLIENT_ID=tu_client_id
LINKEDIN_CLIENT_SECRET=tu_client_secret
LINKEDIN_ACCESS_TOKEN=tu_access_token

# WordPress (opcional)
WORDPRESS_URL=https://tu-sitio.com
WORDPRESS_USERNAME=tu_usuario
WORDPRESS_PASSWORD=tu_password

# Gmail (opcional)
GMAIL_USER=tu_email@gmail.com
GMAIL_APP_PASSWORD=tu_app_password
```

## 📊 Uso

### Generar Contenido
1. Ve a "✏️ Generación"
2. Completa el formulario con los detalles de tu publicación
3. Selecciona las plataformas objetivo
4. Genera el contenido

### Programar Publicaciones
1. Ve a "📝 Publicaciones"
2. Selecciona una publicación guardada
3. Establece fecha y hora de publicación
4. El scheduler la publicará automáticamente

### Ver Historial
1. Ve a "📝 Publicaciones"
2. Pestaña "📜 Historial"
3. Filtra por fecha, plataforma o título

## 🐳 Docker

### Servicios

- `publicador_industrial_web` - Interfaz web Streamlit (Puerto 8504)
- `publicador_industrial_scheduler` - Scheduler automático de publicaciones

### Comandos útiles

```bash
# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios propuestos.

## 📝 Licencia

Este proyecto está bajo licencia MIT.
