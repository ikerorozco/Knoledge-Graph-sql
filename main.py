from api.openaire_api import buscar_por_titulo as buscar_openaire, buscar_organizacion
from api.openalex_api import buscar_por_titulo_openalex

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

def buscar_org(nombre):
    """
    Busca una organización en OpenAIRE.
    
    Args:
        nombre (str): Nombre de la organización a buscar
    """
    print(f"\nBuscando organización: {nombre}")
    return buscar_organizacion(nombre)

if __name__ == "__main__":
    # Ejemplo de uso para papers
    titulo = "Quality over Quantity: Boosting Data Efficiency Through Ensembled Multimodal Data Curation"
    buscar_paper(titulo)
    
    # Ejemplo de uso para organizaciones
    nombre_org = "Universidad de Granada"
    buscar_org(nombre_org)