from apify_client import ApifyClient

# 🔐 Tu API Token de Apify
client = ApifyClient("apify_api_GHXaRAfNdbpqLOAcdyhdfU3o5EbKdB1Teu8t")

# 🔗 URL desde donde se extraerá la info de contacto
run_input = {
    "startUrls": [
        {"url": "https://www.zillow.com/los-angeles-ca-90046/"},
        # Puedes agregar más URLs aquí, una por cada zona
    ],
    "maxRequestsPerStartUrl": 20,
    "maxDepth": 2,
    "maxRequests": 100,
    "sameDomain": True,
    "considerChildFrames": True,
    "useBrowser": False,  # Usa navegador sin headless (más rápido, pero puede fallar con contenido dinámico)
    "waitUntil": "domcontentloaded",
    "proxyConfig": {"useApifyProxy": True},
}

print("🚀 Ejecutando Contact Details Scraper...")
run = client.actor("9Sk4JJhEma9vBKqrg").call(run_input=run_input)

print("\n📄 Resultados encontrados:\n")
for i, item in enumerate(client.dataset(run["defaultDatasetId"]).iterate_items(), start=1):
    emails = item.get("emails", [])
    phones = item.get("phones", [])
    social = item.get("social", [])
    page = item.get("url", "N/A")

    print(f"""
🔢 Resultado #{i}
🌐 Página: {page}
📧 Emails: {emails if emails else 'Ninguno'}
📞 Teléfonos: {phones if phones else 'Ninguno'}
🔗 Redes sociales: {social if social else 'Ninguna'}
    """)
