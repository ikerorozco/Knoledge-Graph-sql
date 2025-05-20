from api.openaire_api import buscar_por_titulo as buscar_openaire
from api.openaire_api import buscar_organizacion,completar_paper_con_api
from api.openalex_api import buscar_por_titulo_openalex
from extractors.grobid_extractor import (
    main as grobid_extractor_main
)
from models.paper import Paper
from models.author import Author
from models.organization import Organization


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

def crear_paper(pdf_data_title,pdf_data_authors,pdf_data_organizations):
    """
    Crea un objeto Paper a partir de los datos de un PDF.
    
    Args:
        pdf_data (dict): Datos del PDF
    """
    paper = Paper(
        title=pdf_data_title,
        autores=crear_autores(pdf_data_authors),
        organization=crear_organizaciones(pdf_data_organizations),
    )
    paper = completar_paper_con_api(paper)
    print(f"Paper creado y enriquecido: {paper.title}")
    print(paper.mostrar_info())
    return paper

def crear_autores(pdf_data_authors):
    autores = []
    for autor_name in pdf_data_authors:
        autor = Author(
            nombre=autor_name,
        )
        autores.append(autor)
    return autores

def crear_organizaciones(pdf_data_organizations):
    organizaciones = []
    for organizacion_name in pdf_data_organizations:
        organizacion = Organization(
            nombre=organizacion_name,
        )
        organizaciones.append(organizacion)
    return organizaciones


if __name__ == "__main__":

    all_pdf_data = grobid_extractor_main()
    papers = []
    for pdf_data in all_pdf_data:
        paper = crear_paper(pdf_data['title'],pdf_data['authors'],pdf_data['organizations'])
        papers.append(paper)

