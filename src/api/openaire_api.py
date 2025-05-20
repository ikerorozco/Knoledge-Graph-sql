import requests
import xml.etree.ElementTree as ET
from models.author import Author
from models.paper import Paper
from models.organization import Organization

def parsear_xml_openaire(xml_data):
    try:
        root = ET.fromstring(xml_data)

        # Título
        titulo_elem = root.find('.//title')
        titulo = titulo_elem.text.strip() if titulo_elem is not None and titulo_elem.text else None

        # DOI
        doi_elem = root.find(".//pid[@classid='doi']")
        doi = doi_elem.text.strip() if doi_elem is not None and doi_elem.text else None

        # Fecha de aceptación
        fecha_elem = root.find('.//dateofacceptance')
        fecha = fecha_elem.text.strip() if fecha_elem is not None and fecha_elem.text else None

        # Idioma
        idioma_elem = root.find(".//language")
        idioma = idioma_elem.text.strip() if idioma_elem is not None and idioma_elem.text else None

        # Veces citado
        citado_elem = root.find(".//citationcount")
        veces_citado = citado_elem.text.strip() if citado_elem is not None and citado_elem.text else None

        # Páginas
        paginas_elem = root.find(".//resourcetype")
        paginas = paginas_elem.get("pages") if paginas_elem is not None and paginas_elem.get("pages") else None

        # RDF Type
        tipo_elem = root.find(".//resourcetype")
        rdf_type = tipo_elem.text.strip() if tipo_elem is not None and tipo_elem.text else None

        # Autores con lógica mejorada
        autores = []
        for creator in root.findall('.//creator'):
            nombre = None
            rdf_type_autor = None
            profesion = None
            trabajos = None

            # Nombre del autor
            name_elem = creator.find('.//creatorName')
            if name_elem is not None and name_elem.text:
                nombre = name_elem.text.strip()
            elif creator.text:
                nombre = creator.text.strip()

            # RDF type
            type_elem = creator.find('.//type')
            if type_elem is not None and type_elem.text:
                rdf_type_autor = type_elem.text.strip()

            # Profesión
            profession_elem = creator.find('.//occupation')
            if profession_elem is not None and profession_elem.text:
                profesion = profession_elem.text.strip()

            # Trabajos previos o afiliaciones
            aff_elem = creator.find('.//affiliation')
            if aff_elem is not None and aff_elem.text:
                trabajos = aff_elem.text.strip()

            autor = Author(nombre=nombre, rdf_type=rdf_type_autor, profesion=profesion, trabajos=trabajos)
            autores.append(autor)

        # Crear instancia del Paper
        paper = Paper(
            title=titulo,
            doi=doi,
            date=fecha,
            idioma=idioma,
            veces_citado=veces_citado,
            paginas=paginas,
            rdf_type=rdf_type,
            autores=autores,
            organization=[]  # <-- Agrega esto
        )

        # print("\n--- Resultado de la búsqueda ---")
        # paper.mostrar_info()
        # print("--- Fin del resultado ---\n")
        return paper

    except ET.ParseError as e:
        print(f"Error al parsear XML: {e}")
        return None

def parsear_json_organizacion_openaire(json_data):
    try:
        organizaciones = []
        resultados = json_data.get("results", [])

        for org_data in resultados:
            # Extraer información básica
            nombre = org_data.get("legalName")
            nombre_corto = org_data.get("legalShortName")
            lugar = org_data.get("country", {}).get("label")
            rdftype = "Organization"  # Tipo por defecto
            trabajos = None  # No disponible en la nueva API
            links = org_data.get("websiteUrl")
            id_org = org_data.get("id")
            nombres_alternativos = org_data.get("alternativeNames", [])

            # Crear objeto Organizacion
            organizacion = Organization(
                nombre=nombre or nombre_corto,
                lugar=lugar,
                rdftype=rdftype,
                trabajos=trabajos,
                links=links
            )
            organizaciones.append(organizacion)

        if organizaciones:
            print("\n--- Resultados de la búsqueda de organizaciones ---")
            print(f"Total de resultados encontrados: {json_data.get('header', {}).get('numFound', 0)}")
            for i, org in enumerate(organizaciones, 1):
                print(f"\nOrganización {i}:")
                org.mostrar_info()
                if nombres_alternativos:
                    print(f"  Nombres alternativos: {', '.join(nombres_alternativos)}")
                if id_org:
                    print(f"  ID: {id_org}")
            print("--- Fin de los resultados ---\n")
            return organizaciones
        else:
            print("No se encontraron organizaciones en los resultados.")
            return None

    except Exception as e:
        print(f"Error al procesar JSON: {e}")
        return None

def buscar_por_titulo(titulo):
    try:
        print(f"\n Buscando en OpenAIRE: {titulo}\n")
        api_url = f"https://api.openaire.eu/search/publications?title={titulo}&format=xml"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            return parsear_xml_openaire(response.text)
        else:
            print(f"Error al consultar OpenAIRE (Error {response.status_code})")
            return None
    except Exception as e:
        print(f"Error al consultar OpenAIRE para '{titulo}': {e}")
        return None
    
from api.openaire_api import buscar_por_titulo

def buscar_autor_en_openaire(nombre_autor):
    """
    Busca un autor por nombre en OpenAIRE y devuelve un objeto Author si lo encuentra.
    """
    try:
        api_url = f"https://api.openaire.eu/search/persons?title={nombre_autor}&format=xml"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            creator = root.find('.//person')
            if creator is not None:
                nombre = creator.findtext('.//fullname') or creator.findtext('.//name')
                rdf_type = creator.findtext('.//type')
                profesion = creator.findtext('.//occupation')
                trabajos = creator.findtext('.//affiliation')
                return Author(
                    nombre=nombre,
                    rdf_type=rdf_type,
                    profesion=profesion,
                    trabajos=trabajos
                )
        return None
    except Exception:
        return None

def completar_paper_con_api(paper):
    """
    Completa los campos vacíos de un objeto Paper usando la API de OpenAIRE.
    Además, valida y completa los autores y organizaciones.
    """

    # Si todos los campos están completos, no hace nada
    campos_faltantes = [
        paper.doi, paper.date, paper.idioma, paper.veces_citado, paper.paginas, paper.rdf_type
    ]
    if all(campo not in [None, ""] for campo in campos_faltantes):
        pass  # Puede haber autores/organizaciones incompletos

    # Buscar información en la API usando el título
    paper_api = buscar_por_titulo(paper.title)

    if paper_api:
        if not paper.doi:
            paper.doi = paper_api.doi
        if not paper.date:
            paper.date = paper_api.date
        if not paper.idioma:
            paper.idioma = paper_api.idioma
        if not paper.veces_citado:
            paper.veces_citado = paper_api.veces_citado
        if not paper.paginas:
            paper.paginas = paper_api.paginas
        if not paper.rdf_type:
            paper.rdf_type = paper_api.rdf_type
        if (not paper.autores or len(paper.autores) == 0) and hasattr(paper_api, "autores"):
            paper.autores = paper_api.autores
        if (not paper.organization or len(paper.organization) == 0) and hasattr(paper_api, "organization"):
            paper.organization = paper_api.organization

    # Validar y completar autores
    autores_validados = []
    for autor in paper.autores:
        autor_completo = buscar_autor_en_openaire(autor.nombre)
        if autor_completo:
            if not autor.rdf_type:
                autor.rdf_type = autor_completo.rdf_type
            if not autor.profesion:
                autor.profesion = autor_completo.profesion
            if not autor.trabajos:
                autor.trabajos = autor_completo.trabajos
            autores_validados.append(autor)
    paper.autores = autores_validados

    # Validar y completar organizaciones
    organizaciones_validadas = []
    for org in getattr(paper, "organization", []):
        # Si org es un string, conviértelo a Organization
        if isinstance(org, str):
            org_obj = Organization(nombre=org, lugar=None, rdftype=None, trabajos=None, links=None)
        else:
            org_obj = org

        resultado = buscar_organizacion(org_obj.nombre)
        if resultado and len(resultado) > 0:
            org_api = resultado[0]
            if not org_obj.lugar:
                org_obj.lugar = org_api.lugar
            if not org_obj.rdftype:
                org_obj.rdftype = org_api.rdftype
            if not org_obj.trabajos:
                org_obj.trabajos = org_api.trabajos
            if not org_obj.links:
                org_obj.links = org_api.links
        # Siempre agrega la organización, aunque no se haya actualizado
        organizaciones_validadas.append(org_obj)
    paper.organization = organizaciones_validadas

    return paper

def buscar_organizacion(nombre, pagina=1, resultados_por_pagina=1):
    """
    Busca organizaciones en OpenAIRE Graph API por nombre.
    
    Args:
        nombre (str): Nombre de la organización a buscar
        pagina (int): Número de página de resultados
        resultados_por_pagina (int): Cantidad de resultados por página
        
    Returns:
        list: Lista de objetos Organizacion encontrados, o None si hay error
    """
    try:
        print(f"\nBuscando organización en OpenAIRE: {nombre}\n")
        api_url = f"https://api.openaire.eu/graph/v1/organizations"
        params = {
            "search": nombre,
            "page": pagina,
            "pageSize": resultados_por_pagina,
            "sortBy": "relevance DESC"
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            return parsear_json_organizacion_openaire(response.json())
        else:
            print(f"Error al consultar OpenAIRE (Error {response.status_code})")
            return None
    except Exception as e:
        print(f"Error al consultar OpenAIRE para la organización '{nombre}': {e}")
        return None