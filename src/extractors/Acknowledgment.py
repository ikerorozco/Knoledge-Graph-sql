import os
import sys
import argparse
import requests
import xml.etree.ElementTree as ET
from transformers import pipeline
from models.organization import Organization

# Configurar salida UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Argumentos de entrada
parser = argparse.ArgumentParser(description="Extraer el acknowledgment de PDFs usando GROBID.")
parser.add_argument("-i", "--input", default="data", help="Carpeta que contiene los archivos PDF.")
args = parser.parse_args()
PDF_DIRECTORY = args.input

if not os.path.exists(PDF_DIRECTORY):
    print(f"La carpeta '{PDF_DIRECTORY}' no existe.")
    exit(1)

# Endpoint de GROBID
GROBID_URL = "http://localhost:8070/api/processFulltextDocument"

# Configurar el modelo NER de Hugging Face (solo cargar una vez)
ner_pipeline = pipeline(
    "ner",
    model="Jean-Baptiste/roberta-large-ner-english",
    aggregation_strategy="simple"
)

# Namespaces TEI
namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}

#------------------------------------------------------
# Funciones para extraer datos desde XML GROBID
def extract_acknowledgment(root):
    ack_texts = []
    for div in root.findall(".//tei:div[@type='acknowledgement']", namespaces):
        text = " ".join(p.strip() for p in div.itertext())
        if text:
            ack_texts.append(text.strip())
    return " ".join(ack_texts).strip()

def extract_organizations_from_acknowledgment(acknowledgment_text):
    # Usar el modelo NER de Hugging Face para detectar las organizaciones
    entities = ner_pipeline(acknowledgment_text)
    
    organizations = {ent["word"]                    
                     for ent in entities
                     if ent["entity_group"] == "ORG"   # sólo entidades de tipo ORG
       and ent["score"] >= 0.85       # umbral de confianza
    }


    return organizations

def agregar_organizaciones_de_acknowledgment_a_paper(paper, pdf_path, grobid_url="http://localhost:8070/api/processFulltextDocument"):
    """
    Procesa el acknowledgment del PDF y agrega organizaciones detectadas al objeto Paper.
    Args:
        paper (Paper): Objeto Paper a complementar.
        pdf_path (str): Ruta al archivo PDF.
        grobid_url (str): Endpoint de GROBID.
    """
    with open(pdf_path, "rb") as f:
        response = requests.post(grobid_url, files={"input": f}, data={"consolidate": "1"})

    if response.status_code != 200:
        print(f"    Error {response.status_code} al procesar {pdf_path}")
        return

    try:
        root = ET.fromstring(response.text)
        acknowledgment = extract_acknowledgment(root)

        if acknowledgment:
            print(f"Acknowledgment extraído de {os.path.basename(pdf_path)}:")
            print(acknowledgment)

            organizations = extract_organizations_from_acknowledgment(acknowledgment)
            if organizations:
                print("Organizaciones detectadas:")
                for org_name in organizations:
                    print(f"  - {org_name}")
                    # Evitar duplicados
                    if not any(org.nombre == org_name for org in paper.organization):
                        paper.organization.append(Organization(nombre=org_name))
            else:
                print("No se detectaron organizaciones en el acknowledgment.")
        else:
            print(f"No se encontró acknowledgment en {os.path.basename(pdf_path)}.")

    except ET.ParseError as e:
        print(f"    Error al analizar XML: {e}")

# Procesar los archivos PDF
pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.lower().endswith(".pdf")]
if not pdf_files:
    print("No hay archivos PDF en la carpeta.")
    exit(1)

for pdf in pdf_files:
    print(f"\nProcesando: {pdf}")
    pdf_path = os.path.join(PDF_DIRECTORY, pdf)

    with open(pdf_path, "rb") as f:
        response = requests.post(GROBID_URL, files={"input": f}, data={"consolidate": "1"})

    if response.status_code != 200:
        print(f"    Error {response.status_code} al procesar {pdf}")
        continue

    try:
        root = ET.fromstring(response.text)
        acknowledgment = extract_acknowledgment(root)

        if acknowledgment:
            print(f"Acknowledgment extraído de {pdf}:")
            print(acknowledgment)

            # Detectar organizaciones en el acknowledgment usando Hugging Face
            organizations = extract_organizations_from_acknowledgment(acknowledgment)

            if organizations:
                print("Organizaciones detectadas:")
                for org in organizations:
                    print(f"  - {org}")
            else:
                print("No se detectaron organizaciones en el acknowledgment.")
        else:
            print(f"No se encontró acknowledgment en {pdf}.")

    except ET.ParseError as e:
        print(f"    Error al analizar XML: {e}")
