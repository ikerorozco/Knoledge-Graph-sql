from api.openaire_api import buscar_por_titulo as buscar_openaire
from api.openaire_api import buscar_organizacion, completar_paper_con_openaire, buscar_proyectos_asociados_paper
from api.openalex_api import buscar_por_titulo_openalex
from extractors.grobid_extractor import (
    main as grobid_extractor_main,
    generar_embeddings_y_similitud,
    get_all_pdf_data
    
)
from models.paper import Paper
from models.author import Author
from models.organization import Organization
from graph.graph_creator import create_knowledge_graph    

# Creacion de objetos
def crear_papers_inicial(all_pdf_data):
    papers = []
    for pdf_data in all_pdf_data:
        paper = crear_paper(pdf_data['title'], pdf_data['authors'], pdf_data['organizations'])
        papers.append(paper)
    return papers

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
    paper = completar_paper_con_openaire(paper)
    #print(f"Paper creado y enriquecido con openaire: {paper.title}")
    #paper.mostrar_info()
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


# Enriquecimiento de papers
def enriquecer_papers_openalex(papers):
    for paper in papers:
        buscar_por_titulo_openalex(paper)
        #print(f"Paper enriquecido con openalex: {paper.title}")
        #paper.mostrar_info()

def obtener_proyectos_asociados(papers):
    """
    Busca todos los proyectos asociados a una lista de papers.
    
    Args:
        papers (list): Lista de objetos Paper
        
    Returns:
        list: Lista de objetos Project asociados a los papers
    """
    todos_proyectos = []
    
    print("\n=== Buscando proyectos asociados a los papers ===")
    for i, paper in enumerate(papers, 1):
        print(f"\nProcesando paper {i}/{len(papers)}: {paper.title}")
        
        # Buscar proyectos asociados a este paper
        proyectos = buscar_proyectos_asociados_paper(paper)
        # Añadir los proyectos encontrados a la lista general
        todos_proyectos.extend(proyectos)
    
    # Mostrar resumen final
    print(f"\n=== Resumen de proyectos encontrados ===")
    print(f"Total de papers procesados: {len(papers)}")
    print(f"Total de proyectos encontrados: {len(todos_proyectos)}")
    
    return todos_proyectos


if __name__ == "__main__":

    all_pdf_data = grobid_extractor_main()
    papers = crear_papers_inicial(all_pdf_data) # contiene papers (enriquecidos con openaire) con autores (enriquecidos con openaire) y organizaciones
    enriquecer_papers_openalex(papers) # enriquecimiento de papers con openalex
    # Obtener proyectos asociados a los papers
    proyectos = obtener_proyectos_asociados(papers)
    
    # Generar embeddings y similitud entre papers
    generar_embeddings_y_similitud(get_all_pdf_data(), papers_objetos=papers)
    
    # Crear el grafo de conocimiento
    kg = create_knowledge_graph(papers, proyectos)
    
    # Visualizar el grafo y guardar la imagen
    print("\n=== Creando visualización del grafo de conocimiento ===")
    graph_image_path = kg.visualize(save_path="knowledge_graph.png")
    print(f"Grafo guardado como imagen en: {graph_image_path}")

    # # Mostrar información de los papers parecidos
    # print("\n=== Papers parecidos encontrados ===")
    # for paper in papers:
    #     if paper.parecido:
    #         print(f"\nPaper: {paper.title}")
    #         print("  Parecidos:")
    #         for parecido in paper.parecido:
    #             print(f"    - {parecido.title}")
                
    # for paper in papers:
    #     buscar_por_titulo_openalex(paper)
        
    # # Mostrar información completa de los autores de cada paper
    # print("\n=== Información completa de los autores de cada paper ===")
    # for paper in papers:
    #     print(f"\nPaper: {paper.title}")
    #     if paper.autores:
    #         for autor in paper.autores:
    #             print(f"  Autor: {getattr(autor, 'nombre', 'Desconocido')}")
    #             print(f"    Tipo: {getattr(autor, 'rdf_type', 'Desconocido')}")
    #             print(f"    Profesión: {getattr(autor, 'profesion', 'Desconocido')}")
    #             print(f"    Trabajos: {getattr(autor, 'trabajos', 'Desconocido')}")
    #     else:
    #         print("  No hay autores registrados.")
            
    # # Mostrar información completa de las organizaciones de cada paper
    # print("\n=== Información completa de las organizaciones de cada paper ===")
    # for paper in papers:
    #     print(f"\nPaper: {paper.title}")
    #     if paper.organization:
    #         for org in paper.organization:
    #             print(f"  Organización: {getattr(org, 'nombre', 'Desconocido')}")
    #             print(f"    Tipo: {getattr(org, 'rdftype', 'Desconocido')}")
    #             print(f"    País: {getattr(org, 'lugar', 'Desconocido')}")
    #             print(f"    Trabajos: {getattr(org, 'trabajos', 'Desconocido')}")
    #             print(f"    Enlace: {getattr(org, 'links', 'Desconocido')}")
    #     else:
    #         print("  No hay organizaciones registradas.")
