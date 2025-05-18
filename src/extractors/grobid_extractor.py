import os
import sys
import requests
import xml.etree.ElementTree as ET
from models.author import Author


# Configurar salida UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Endpoint de GROBID
GROBID_URL = "http://localhost:8070/api/processFulltextDocument"

# Namespaces TEI
namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}

def extract_title(root):
    el = root.find(".//tei:titleStmt/tei:title", namespaces)
    return el.text.strip() if el is not None and el.text else "Desconocido"

def extract_authors(root):
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

def extract_organizations(root):
    orgs = set()
    for aff in root.findall(".//tei:affiliation", namespaces):
        org_el = aff.find(".//tei:orgName", namespaces)
        if org_el is not None and org_el.text:
            orgs.add(org_el.text.strip())
    return list(orgs)

def extract_project(root):
    funders = []
    for fund in root.findall(".//tei:funding", namespaces):
        proj = fund.find(".//tei:orgName", namespaces)
        if proj is not None and proj.text:
            funders.append(proj.text.strip())
    return funders

def extract_page_count(root):
    refs = root.findall(".//tei:pb", namespaces)
    return len(refs)

def extract_acknowledgment(root):
    ack_texts = []
    for div in root.findall(".//tei:div[@type='acknowledgement']", namespaces):
        text = " ".join(p.strip() for p in div.itertext())
        if text:
            ack_texts.append(text.strip())
    return " ".join(ack_texts).strip()

def process_pdf(pdf_path):
    """
    Procesa un archivo PDF usando GROBID y extrae su información.
    
    Args:
        pdf_path (str): Ruta al archivo PDF
        
    Returns:
        Paper: Objeto Paper con la información extraída
    """
    with open(pdf_path, "rb") as f:
        response = requests.post(GROBID_URL, files={"input": f}, data={"consolidate": "1"})

    if response.status_code != 200:
        print(f"    Error {response.status_code} al procesar {pdf_path}")
        return None

    try:
        root = ET.fromstring(response.text)
        title = extract_title(root)
        authors = extract_authors(root)
        organizations = extract_organizations(root)
        project = extract_project(root)
        page_count = extract_page_count(root)
        acknowledgment = extract_acknowledgment(root)

        # Crear objetos Author para cada autor encontrado
        autores_objs = []
        for nombre_autor in authors:
            autor_obj = Author(
                nombre=nombre_autor,
                rdf_type="foaf:Person",
                profesion="Investigador/a",
                trabajos=None
            )
            autores_objs.append(autor_obj)

        # Crear el objeto Paper
        paper_obj = Paper(
            title=title,
            doi="Desconocido",
            date="Desconocida",
            idioma="Desconocido",
            veces_citado=None,
            paginas=page_count,
            rdf_type="bibo:AcademicArticle",
            autores=autores_objs
        )

        return paper_obj

    except ET.ParseError as e:
        print(f"    Error al analizar XML: {e}")
        return None 