import os
import sys
import argparse
import requests
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

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



def Grobid_extract_acknowledgment(root):
    ack_texts = []
    for div in root.findall(".//tei:div[@type='acknowledgement']", namespaces):
        text = " ".join(p.strip() for p in div.itertext())
        if text:
            ack_texts.append(text.strip())
    return " ".join(ack_texts).strip()

# Lista para almacenar los datos de todos los PDFs
all_pdf_data = []

def process_pdfs(pdf_directory="data/raw", grobid_url="http://localhost:8070/api/processFulltextDocument"):
    """
    Procesa los archivos PDF en el directorio especificado utilizando GROBID.
    
    Args:
        pdf_directory (str): Directorio que contiene los archivos PDF
        grobid_url (str): URL del endpoint de GROBID
        
    Returns:
        list: Lista de diccionarios con los datos extraídos de cada PDF
    """
    global all_pdf_data
    all_pdf_data = []
    
    # Verificar si la ruta es relativa y convertirla a ruta absoluta basada en la raíz del proyecto
    if not os.path.isabs(pdf_directory):
        # Encontrar la raíz del proyecto (2 niveles hacia arriba desde este script)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pdf_directory = os.path.join(project_root, pdf_directory)

    if not os.path.exists(pdf_directory):
        print(f"La carpeta '{pdf_directory}' no existe.")
        return []

    # Crear directorio para guardar las respuestas XML si no existe
    output_dir = os.path.join(os.path.dirname(pdf_directory), "xml_responses")
    os.makedirs(output_dir, exist_ok=True)
    
    # Procesar los archivos PDF
    pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("No hay archivos PDF en la carpeta.")
        return []

    for pdf in pdf_files:
        print(f"\n Procesando: {pdf}")
        pdf_path = os.path.join(pdf_directory, pdf)

        with open(pdf_path, "rb") as f:
            response = requests.post(grobid_url, files={"input": f}, data={"consolidate": "1"})

        if response.status_code != 200:
            print(f" Error {response.status_code} al procesar {pdf}")
            continue

        try:
            # Guardar la respuesta XML en un archivo
            xml_filename = os.path.splitext(pdf)[0] + ".xml"
            xml_path = os.path.join(output_dir, xml_filename)
            with open(xml_path, "w", encoding="utf-8") as xml_file:
                xml_file.write(response.text)
            print(f"     Respuesta XML guardada en: {xml_path}")
            
            root = ET.fromstring(response.text)
            
            # Almacenar los datos en un diccionario
            pdf_data = {
                "filename": pdf,
                "title": Grobid_extract_title(root),
                "authors": Grobid_extract_authors(root),
                "organizations": Grobid_extract_organizations(root),
                "acknowledgment": Grobid_extract_acknowledgment(root)
            }
            
            # Agregar el diccionario a la lista
            all_pdf_data.append(pdf_data)
            
            # Opcional: Mostrar un resumen de los datos extraídos
            print(f"     Título: {pdf_data['title']}")
            print(f"     # Autores: {len(pdf_data['authors'])}")
            print(f"     Organizaciones: {', '.join(pdf_data['organizations'])}")
            print(f"     Agradecimientos: {pdf_data['acknowledgment']}")

        except ET.ParseError as e:
            print(f"     Error al analizar XML: {e}")
            
    return all_pdf_data

# Funciones normalizadas que devuelven los datos de todos los PDFs
def Grobid_extract_title_Normalizado():
    return [pdf_data["title"] for pdf_data in all_pdf_data]

def Grobid_extract_authors_Normalizado():
    return [pdf_data["authors"] for pdf_data in all_pdf_data]

def Grobid_extract_organizations_Normalizado():
    return [pdf_data["organizations"] for pdf_data in all_pdf_data]


def get_all_pdf_data():
    return all_pdf_data

def main():
    """Función principal que ejecuta la extracción de datos de PDFs"""
    parser = argparse.ArgumentParser(description="Extraer metadatos desde PDFs usando GROBID.")
    parser.add_argument("-i", "--input", default="data/raw", help="Carpeta que contiene los archivos PDF.")
    args = parser.parse_args()
    
    process_pdfs(pdf_directory=args.input)
    
    # Aquí podrías agregar más código para procesar o guardar los datos extraídos
    
    return all_pdf_data
