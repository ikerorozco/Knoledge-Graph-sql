import os
import sys
import argparse
import requests
import xml.etree.ElementTree as ET
from transformers import pipeline

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

# Namespaces TEI
namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}

#------------------------------------------------------
# Cargar el modelo NER de Hugging Face (mejorado)
ner_pipeline = pipeline(
    "ner",
    model="Jean-Baptiste/roberta-large-ner-english",
    aggregation_strategy="simple"
)


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
