from api.openaire_api import buscar_por_titulo as buscar_openaire
from api.openaire_api import buscar_organizacion
from api.openalex_api import buscar_por_titulo_openalex
from extractors.grobid_extractor import process_pdf
from models import paper, organization, author
from extractors.grobid_extractor import (
    Grobid_extract_title,
    Grobid_extract_authors,
    Grobid_extract_organizations,
    Grobid_extract_project,
    Grobid_extract_page_count,
)

paperObj= paper()
papers = []
authorObj= author()
authors = []
organizationObj= organization()
organizations = []


def buscar_paper(titulo):
    """
    Busca un paper en ambas APIs y muestra los resultados.
    
    Args:
        titulo (str): Título del paper a buscar
    """
    print(f"\nBuscando paper: {titulo}")
    print("\n=== Resultados de OpenAIRE ===")
    paper_openaire = buscar_openaire(titulo)
    
    print("\n=== Resultados de OpenAlex ===")
    paper_openalex = buscar_por_titulo_openalex(titulo)
    
    return paper_openaire, paper_openalex

def buscar_org(nombre, pagina=1, resultados_por_pagina=10):
    """
    Busca una organización en OpenAIRE.
    
    Args:
        nombre (str): Nombre de la organización a buscar
        pagina (int): Número de página de resultados
        resultados_por_pagina (int): Cantidad de resultados por página
    """
    print(f"\nBuscando organización: {nombre}")
    return buscar_organizacion(nombre, pagina, resultados_por_pagina)

import os
import xml.etree.ElementTree as ET

PDF_DIRECTORY = "data"

def procesar_pdfs_en_carpeta(pdf_directory):
    papers = []
    authors = []

    for pdf_file in os.listdir(pdf_directory):
        if not pdf_file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(pdf_directory, pdf_file)
        print(f"\nProcesando: {pdf_file}")

        # Procesar PDF con GROBID
        import requests
        GROBID_URL = "http://localhost:8070/api/processFulltextDocument"
        with open(pdf_path, "rb") as f:
            response = requests.post(GROBID_URL, files={"input": f}, data={"consolidate": "1"})
        if response.status_code != 200:
            print(f" Error {response.status_code} al procesar {pdf_file}")
            continue

        try:
            root = ET.fromstring(response.text)
            title = Grobid_extract_title(root)
            author_names = Grobid_extract_authors(root)
            # Crear objetos Author
            autores = [Author(nombre=nombre) for nombre in author_names]
            authors.extend(autores)
            paper = Paper(
                title=title,
                doi=None,
                date=None,
                idioma=None,
                veces_citado=None,
                paginas=Grobid_extract_page_count(root),
                rdf_type=None,
                autores=autores
            )
            papers.append(paper)
        except ET.ParseError as e:
            print(f"     Error al analizar XML: {e}")

    return papers, authors

if __name__ == "__main__":
    # Ejemplo de uso para papers
    titulo = "Quality over Quantity: Boosting Data Efficiency Through Ensembled Multimodal Data Curation"
    buscar_paper(titulo)
    
    # Ejemplo de uso para organizaciones
    nombre_org = "Complutense"
    # Buscar primera página con 5 resultados
    buscar_org(nombre_org, pagina=1, resultados_por_pagina=5)

    papers, authors = procesar_pdfs_en_carpeta(PDF_DIRECTORY)

    print("\n=== Resultados de Papers ===")
    for paper in papers:
        paper.mostrar_info()

    print("\n=== Resultados de Autores ===")
    for author in authors:
        author.mostrar_info()