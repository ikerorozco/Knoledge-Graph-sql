from api.openaire_api import buscar_por_titulo as buscar_openaire
from api.openaire_api import buscar_organizacion
from api.openalex_api import buscar_por_titulo_openalex
from extractors.grobid_extractor import get_all_pdf_data

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

if __name__ == "__main__":
    # Ejemplo de uso para papers
    titulo = "Quality over Quantity: Boosting Data Efficiency Through Ensembled Multimodal Data Curation"
    buscar_paper(titulo)
    
    # Ejemplo de uso para organizaciones
    nombre_org = "Complutense"
    # Buscar primera página con 5 resultados
    buscar_org(nombre_org, pagina=1, resultados_por_pagina=5)

    # Ejecutar el extractor Grobid
    get_all_pdf_data()