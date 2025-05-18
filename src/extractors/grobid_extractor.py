import os
import sys
import argparse
import requests
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

# Argumentos de entrada
parser = argparse.ArgumentParser(description="Extraer metadatos desde PDFs usando GROBID.")
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

# Funciones para extraer datos desde XML GROBID
def Grobid_extract_title(root):
    el = root.find(".//tei:titleStmt/tei:title", namespaces)
    return el.text.strip() if el is not None and el.text else "Desconocido"


def Grobid_extract_authors(root):
    authors = []
    for author in root.findall(".//tei:author", namespaces):
        name_el = author.find(".//tei:persName", namespaces)
        if name_el is not None:
            full = " ".join(filter(None, [
                name_el.findtext("tei:forename", default="", namespaces=namespaces),
                name_el.findtext("tei:surname", default="", namespaces=namespaces)
            ])).strip()
            if full:
                authors.append(full)
    return authors

def Grobid_extract_organizations(root):
    orgs = set()
    for aff in root.findall(".//tei:affiliation", namespaces):
        org_el = aff.find(".//tei:orgName", namespaces)
        if org_el is not None and org_el.text:
            orgs.add(org_el.text.strip())
    return list(orgs)

def Grobid_extract_project(root):
    funders = []
    for fund in root.findall(".//tei:funding", namespaces):
        proj = fund.find(".//tei:orgName", namespaces)
        if proj is not None and proj.text:
            funders.append(proj.text.strip())
    return funders

def Grobid_extract_page_count(root):
    refs = root.findall(".//tei:pb", namespaces)
    return len(refs)

def Grobid_extract_acknowledgment(root):
    ack_texts = []
    for div in root.findall(".//tei:div[@type='acknowledgement']", namespaces):
        text = " ".join(p.strip() for p in div.itertext())
        if text:
            ack_texts.append(text.strip())
    return " ".join(ack_texts).strip()

# Procesar los archivos PDF
pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.lower().endswith(".pdf")]
if not pdf_files:
    print("No hay archivos PDF en la carpeta.")
    exit(1)

for pdf in pdf_files:
    print(f"\n Procesando: {pdf}")
    pdf_path = os.path.join(PDF_DIRECTORY, pdf)

    with open(pdf_path, "rb") as f:
        response = requests.post(GROBID_URL, files={"input": f}, data={"consolidate": "1"})

    if response.status_code != 200:
        print(f" Error {response.status_code} al procesar {pdf}")
        continue

    try:
        root = ET.fromstring(response.text)
        title = Grobid_extract_title(root)
        authors = Grobid_extract_authors(root)
        organizations = Grobid_extract_organizations(root)
        project = Grobid_extract_project(root)
        page_count = Grobid_extract_page_count(root)
        acknowledgment = Grobid_extract_acknowledgment(root)


    except ET.ParseError as e:
        print(f"     Error al analizar XML: {e}")

def Grobid_extract_title_Normalizado():
    return title
def Grobid_extract_authors_Normalizado():
    return authors
def Grobid_extract_organizations_Normalizado():
    return organizations
def Grobid_extract_project_Normalizado():
    return project
def Grobid_extract_page_count_Normalizado():
    return page_count
