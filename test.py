import os
import requests
import argparse
import xml.etree.ElementTree as ET
from transformers import pipeline
from urllib.parse import quote  # Para codificar nombres en URLs

# Argumentos
parser = argparse.ArgumentParser(description="Extrae metadatos y acknowledgments desde PDFs.")
parser.add_argument("-i", "--input", default="data", help="Carpeta de PDFs.")
args = parser.parse_args()
PDF_DIRECTORY = args.input

if not os.path.exists(PDF_DIRECTORY):
    print(f"La carpeta '{PDF_DIRECTORY}' no existe.")
    exit(1)

GROBID_URL = "http://localhost:8070/api/processFulltextDocument"
API_ORG_LOOKUP = "https://api.openaire.eu/search/organization?title="
ns = {"tei": "http://www.tei-c.org/ns/1.0"}

# Modelo NER
ner_bert = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

def obtener_texto_completo(elemento):
    partes = []
    if elemento.text:
        partes.append(elemento.text.strip())
    for sub in elemento:
        partes.append(obtener_texto_completo(sub))
        if sub.tail:
            partes.append(sub.tail.strip())
    return " ".join(filter(None, partes))

def extraer_metadatos_y_acknowledgments(pdf_path):
    with open(pdf_path, "rb") as f:
        response = requests.post(GROBID_URL, files={"input": f}, data={"consolidate": "1"})

    if response.status_code != 200:
        print(f"Error {response.status_code} al procesar el archivo {pdf_path}")
        return None, None

    try:
        root = ET.fromstring(response.text)
    except ET.ParseError:
        print(f"Error al analizar el XML del archivo {pdf_path}")
        return None, None

    # Título
    title_el = root.find(".//tei:titleStmt/tei:title", ns)
    title = title_el.text.strip() if title_el is not None and title_el.text else "Desconocido"

    # Autores
    authors = []
    for author in root.findall(".//tei:author", ns):
        pers = author.find(".//tei:persName", ns)
        if pers is not None:
            forename = pers.findtext("tei:forename", default="", namespaces=ns)
            surname = pers.findtext("tei:surname", default="", namespaces=ns)
            full_name = f"{forename} {surname}".strip()
            if full_name:
                authors.append(full_name)

    # Acknowledgments
    acknowledgments = ""
    ack_div = root.find(".//tei:back//tei:div[@type='acknowledgement']", ns)
    if ack_div is not None:
        acknowledgments = obtener_texto_completo(ack_div)

    return {"title": title, "authors": authors}, acknowledgments

def buscar_organizacion_en_api(nombre_org):
    try:
        url = API_ORG_LOOKUP + quote(nombre_org)
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data  # Puedes modificar esto según la estructura del JSON
        else:
            return {"error": f"No encontrado (status {resp.status_code})"}
    except Exception as e:
        return {"error": str(e)}

# Procesamiento principal
pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.lower().endswith(".pdf")]
if not pdf_files:
    print("No hay archivos PDF en la carpeta.")
    exit(1)

for pdf in pdf_files:
    print(f"\n Procesando: {pdf}")
    pdf_path = os.path.join(PDF_DIRECTORY, pdf)

    metadatos, acknowledgment = extraer_metadatos_y_acknowledgments(pdf_path)
    if not metadatos:
        continue

    print(f"     Título: {metadatos['title']}")
    print(f"      Autores: {', '.join(metadatos['authors']) if metadatos['authors'] else 'No encontrados'}")

    if acknowledgment:
        print(f"     Acknowledgments:\n    {acknowledgment}")

        # Aplicar NER a los acknowledgments
        entidades = ner_bert(acknowledgment)
        organizaciones = {ent["word"] for ent in entidades if ent["entity_group"] == "ORG"}

        if organizaciones:
            print("     Organizaciones detectadas en los acknowledgments:")
            for org in sorted(organizaciones):
                print(f"      - {org}")

                # 🔎 Consulta a la API
                resultado = buscar_organizacion_en_api(org)
                if "error" in resultado:
                    print(f"           Error al consultar API: {resultado['error']}")
                else:
                    print(f"          Info desde API: {resultado}")
        else:
            print("     No se detectaron organizaciones adicionales.")
    else:
        print("     No se encontró la sección de acknowledgments.")
