import os
import sys
import time
import json
import re
import requests
import mysql.connector
from dotenv import load_dotenv
from openpyxl import Workbook

# --- Cargar variables de entorno ---
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# --- Expresión regular para correos válidos ---
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
INVALID_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf")

def is_valid_email(email):
    return email and not email.lower().endswith(INVALID_EXTENSIONS)

def get_email_from_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            emails = re.findall(EMAIL_REGEX, response.text)
            for email in emails:
                if is_valid_email(email):
                    return email
    except requests.RequestException:
        return None
    return None

# --- Diccionario de sectores y tablas ---
sectores_tablas = {
    "Veterinarias": "veterinarias",
    "Agencias de Turismo": "agencias_turismo",
    "Spas": "spas",
    "Restaurantes": "restaurantes",
    "Hoteles": "hoteles",
    "Gimnasios": "gimnacios",
    "Cafeterías": "cafeterias",
    "Boutiques": "boutiques",
    "Salones de Belleza": "salones_belleza",
    "Barberías": "barberias",
    "Inmobiliarias": "inmobiliarias",
    "Jardinerías": "jardinerias",
    "Estéticas": "esteticas",
    "Tiendas Naturistas": "tiendas_naturistas",
    "Tiendas de Ropa": "tiendas_ropa",
    "Papelerías": "papelerias",
    "Ferreterías": "ferreterias",
    "Clínicas Dentales": "clinicas_dentales",
    "Consultorios Médicos": "consultorios_medicos",
    "Talleres Mecánicos": "talleres_mecanicos",
    "Constructoras": "constructoras"
}

# --- Menú de sectores ---
sectores = list(sectores_tablas.keys())

print("\n🔍 SECTORES DISPONIBLES:")
for i, s in enumerate(sectores, 1):
    print(f"{i}. {s}")
opcion = int(input("\nSelecciona el número del sector a buscar: "))
sector = sectores[opcion - 1]
nombre_tabla = sectores_tablas[sector]

estado = input("📍 Estado o ciudad: ").strip()
coordenadas = input("📌 Coordenadas (lat,lng): ").strip()
limite = int(input("🔢 Límite de resultados: "))

query = f"{sector} en {estado}"
URL = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={coordenadas}&key={API_KEY}"

places = []
total_results = 0

# --- Conexión a MySQL ---
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
except Exception as e:
    print("❌ Error al conectar con MySQL:", e)
    sys.exit()

# --- Extracción de datos desde Google Places ---
while URL and total_results < limite:
    response = requests.get(URL)
    data = response.json()

    for place in data.get("results", []):
        if total_results >= limite:
            break

        place_id = place["place_id"]
        name = place["name"]
        address = place.get("formatted_address", "No disponible")

        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_address,formatted_phone_number,website,opening_hours,rating,user_ratings_total,geometry&key={API_KEY}"
        details_response = requests.get(details_url)
        details_data = details_response.json().get("result", {})

        phone = details_data.get("formatted_phone_number", "No disponible")
        website = details_data.get("website", "No disponible")
        rating = details_data.get("rating", "No disponible")
        total_reviews = details_data.get("user_ratings_total", "No disponible")
        hours = details_data.get("opening_hours", {}).get("weekday_text", "No disponible")
        lat = details_data.get("geometry", {}).get("location", {}).get("lat", "No disponible")
        lng = details_data.get("geometry", {}).get("location", {}).get("lng", "No disponible")

        email = get_email_from_website(website) if website != "No disponible" else None
        email = email if email else "No disponible"

        if phone != "No disponible" or email != "No disponible":
            # Verificar duplicado en la tabla correspondiente
            cursor.execute(f"SELECT * FROM {nombre_tabla} WHERE nombre = %s AND direccion = %s", (name, address))
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(f"""
                    INSERT INTO {nombre_tabla}
                    (nombre, resenas_totales, telefono, website, calificacion, direccion, latitud, longitud, correo_electronico)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    name, total_reviews, phone, website, rating,
                    address, lat, lng, email
                ))
                conn.commit()
                print(f"✅ Insertado: {name}")
            else:
                print(f"⚠️ Duplicado omitido: {name}")

            places.append({
                "nombre": name,
                "reseñas_totales": total_reviews,
                "telefono": phone,
                "website": website,
                "calificacion": rating,
                "direccion": address,
                "latitud": lat,
                "longitud": lng,
                "correo": email
            })

            total_results += 1

    next_page_token = data.get("next_page_token")
    if next_page_token and total_results < limite:
        URL = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={coordenadas}&key={API_KEY}&pagetoken={next_page_token}"
        time.sleep(2)
    else:
        URL = None

# --- Guardar en archivo Excel ---
if places:
    wb = Workbook()
    ws = wb.active
    ws.title = "Resultados Google"

    headers = ["Nombre", "Reseñas Totales", "Teléfono", "Website", "Calificación", "Dirección", "Latitud", "Longitud", "Correo Electrónico"]
    ws.append(headers)

    for p in places:
        ws.append([
            p["nombre"], p["reseñas_totales"], p["telefono"], p["website"],
            p["calificacion"], p["direccion"], p["latitud"], p["longitud"], p["correo"]
        ])

    nombre_archivo = f"resultados_{nombre_tabla}_{estado}.xlsx"
    wb.save(nombre_archivo)
    print(f"\n📁 Archivo Excel generado: {nombre_archivo}")
else:
    print("\n⚠️ No se encontraron registros para guardar.")

# --- Cierre ---
cursor.close()
conn.close()
