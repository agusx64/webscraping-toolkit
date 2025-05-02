# 📍 Buscador de Empresas con Google Maps API y Selenium

Este proyecto es un script de consola en Python diseñado para buscar negocios en una ubicación geográfica específica utilizando la **API de Google Places**, y extraer información como nombre, dirección, teléfono, sitio web y correo electrónico.

Además, los datos recopilados se almacenan automáticamente en una base de datos **MySQL** y también se exportan a un archivo **Excel (.xlsx)**.

---

## 🚀 Tecnologías utilizadas

- Python 3
- Google Places API
- Selenium
- BeautifulSoup
- Pandas
- Requests
- MySQL Connector
- Openpyxl
- dotenv

---

## ⚙️ Funcionalidades principales

- Búsqueda de empresas por sector (veterinarias, restaurantes, gimnasios, etc.).
- Consulta de resultados por ciudad/estado y coordenadas.
- Obtención de detalles de contacto (teléfono, sitio web, correo).
- Extracción automática de correos electrónicos desde los sitios web encontrados.
- Almacenamiento en MySQL con verificación para evitar duplicados.
- Exportación de los datos a un archivo Excel.
- Menú interactivo de consola.

---

## 🧠 Estructura de funcionamiento

1. Seleccionas un sector (por ejemplo: Spas, Restaurantes, Boutiques).
2. Ingresas el estado o ciudad y coordenadas geográficas.
3. El script consulta los resultados mediante la API de Google Places.
4. Para cada lugar:
   - Extrae detalles (nombre, dirección, teléfono, web, calificación).
   - Obtiene el correo electrónico desde el sitio web si está disponible.
   - Almacena el registro en MySQL y en Excel (evitando duplicados).
5. Genera un archivo Excel con todos los resultados encontrados.

---

## 🔐 Variables de entorno necesarias (`.env`)

Crea un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```env
GOOGLE_API_KEY=tu_api_key_de_google
DB_HOST=localhost
DB_USER=tu_usuario_mysql
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=nombre_de_base_de_datos
```

## 💻 Ejecución
```
python google_scraper.py
```

## 📁 Resultado

Al finalizar, el script generará un archivo `.xlsx` con los datos y los almacenará en una tabla correspondiente dentro de tu base de datos.

## 📝 Ejemplo de sectores disponibles
- Veterinarias
- Agencias de Turismo
- Restaurantes
- Hoteles
- Spas
- Boutiques
- Salones de Belleza
- Consultorios Médicos
- Inmobiliarias
- Clínicas Dentales

## 💡 Nota
- Este script puede ampliarse fácilmente para nuevos sectores.
- Ideal para crear bases de datos de leads, análisis de mercado o localización de clientes potenciales.

## 🤝 Autor

**Agustín Mora Trinidad**  
Desarrollador Full Stack | Web Scraping | Automatización  
🔗 [LinkedIn](https://www.linkedin.com/in/agustin-mora-trinidad-8a733a2b1) | 🌐 [Portafolio](https://agustin-mora.fly.dev/)
