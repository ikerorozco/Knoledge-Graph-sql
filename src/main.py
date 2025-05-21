from api.openaire_api import buscar_por_titulo as buscar_openaire
from api.openaire_api import buscar_organizacion,completar_paper_con_api
from api.openalex_api import buscar_por_titulo_openalex
from extractors.grobid_extractor import (
    main as grobid_extractor_main,
    generar_embeddings_y_similitud,
    get_all_pdf_data
    
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
        paper = crear_paper(pdf_data['title'], pdf_data['authors'], pdf_data['organizations'])
        papers.append(paper)
        
    generar_embeddings_y_similitud(get_all_pdf_data(), papers_objetos=papers)

    # Mostrar información de los papers parecidos
    print("\n=== Papers parecidos encontrados ===")
    for paper in papers:
        if paper.parecido:
            print(f"\nPaper: {paper.title}")
            print("  Parecidos:")
            for parecido in paper.parecido:
                print(f"    - {parecido.title}")
                
    for paper in papers:
        buscar_por_titulo_openalex(paper)
        
    # Mostrar información completa de los autores de cada paper
    print("\n=== Información completa de los autores de cada paper ===")
    for paper in papers:
        print(f"\nPaper: {paper.title}")
        if paper.autores:
            for autor in paper.autores:
                print(f"  Autor: {getattr(autor, 'nombre', 'Desconocido')}")
                print(f"    Tipo: {getattr(autor, 'rdf_type', 'Desconocido')}")
                print(f"    Profesión: {getattr(autor, 'profesion', 'Desconocido')}")
                print(f"    Trabajos: {getattr(autor, 'trabajos', 'Desconocido')}")
        else:
            print("  No hay autores registrados.")
            
    # Mostrar información completa de las organizaciones de cada paper
    print("\n=== Información completa de las organizaciones de cada paper ===")
    for paper in papers:
        print(f"\nPaper: {paper.title}")
        if paper.organization:
            for org in paper.organization:
                print(f"  Organización: {getattr(org, 'nombre', 'Desconocido')}")
                print(f"    Tipo: {getattr(org, 'rdftype', 'Desconocido')}")
                print(f"    País: {getattr(org, 'lugar', 'Desconocido')}")
                print(f"    Trabajos: {getattr(org, 'trabajos', 'Desconocido')}")
                print(f"    Enlace: {getattr(org, 'links', 'Desconocido')}")
        else:
            print("  No hay organizaciones registradas.")
