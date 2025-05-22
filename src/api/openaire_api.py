import requests
import xml.etree.ElementTree as ET
from models.author import Author
from models.paper import Paper
from models.organization import Organization
from models.project import Project
from datetime import datetime

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

def completar_paper_con_openaire(paper):
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

def buscar_proyectos_por_titulo(paper):
    """
    Busca un paper por título en OpenAIRE y extrae los IDs de los proyectos asociados.
    
    Args:
        paper (Paper): Objeto Paper con el título a buscar
        
    Returns:
        list: Lista de IDs de proyectos únicos encontrados
    """
    try:
        titulo = paper.title
        print(f"\nBuscando proyectos en OpenAIRE para el paper: {titulo}\n")
        
        api_url = f"https://api.openaire.eu/search/publications?title={titulo}&format=xml"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code != 200:
            print(f"Error al consultar OpenAIRE (Error {response.status_code})")
            return []
            
        # Parsear el XML de respuesta
        root = ET.fromstring(response.text)
        
        # Buscar todos los IDs de proyectos en la respuesta
        proyecto_ids = []
        
        # Buscar relaciones del tipo "isProducedBy" con proyectos
        for rel in root.findall('.//rel'):
            to_elem = rel.find('./to[@class="isProducedBy"][@type="project"]')
            if to_elem is not None:
                proyecto_id = to_elem.text.strip()
                if proyecto_id and proyecto_id not in proyecto_ids:
                    proyecto_ids.append(proyecto_id)
        
        if proyecto_ids:
            print(f"Se encontraron {len(proyecto_ids)} proyectos asociados al paper.")
        else:
            print("No se encontraron proyectos asociados al paper.")
            
        return proyecto_ids
        
    except ET.ParseError as e:
        print(f"Error al parsear XML: {e}")
        return []
    except Exception as e:
        print(f"Error al buscar proyectos: {e}")
        return []

def buscar_proyecto_por_id(proyecto_id, paper=None):
    """
    Busca un proyecto por su ID en OpenAIRE y crea un objeto Project con la información.
    
    Args:
        proyecto_id (str): ID del proyecto a buscar
        paper (Paper, optional): Objeto Paper a asociar con el proyecto. Defaults to None.
        
    Returns:
        Project: Objeto Project con la información del proyecto, o None si hay error
    """
    try:
        print(f"\nBuscando proyecto en OpenAIRE con ID: {proyecto_id}\n")
        
        api_url = f"https://api.openaire.eu/graph/v1/projects"
        params = {
            "id": proyecto_id,
            "page": 1,
            "pageSize": 1,
            "sortBy": "relevance DESC"
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"Error al consultar OpenAIRE (Error {response.status_code})")
            return None
            
        # Parsear el JSON de respuesta
        data = response.json()
        
        # Verificar si hay resultados
        resultados = data.get("results", [])
        if not resultados:
            print("No se encontró el proyecto con el ID proporcionado.")
            return None
            
        # Obtener el primer resultado (debería ser único por ID)
        proyecto_data = resultados[0]
        
        # Extraer información básica del proyecto
        nombre = proyecto_data.get("title")
        funded_amount = None
        start_date = None
        end_date = None
        
        # Obtener monto financiado
        granted = proyecto_data.get("granted", {})
        if granted and "fundedAmount" in granted:
            funded_amount = float(granted["fundedAmount"])
        
        # Convertir fechas de string a objeto date
        if proyecto_data.get("startDate"):
            try:
                start_date = datetime.strptime(proyecto_data.get("startDate"), "%Y-%m-%d").date()
            except ValueError:
                print(f"Error al convertir la fecha de inicio: {proyecto_data.get('startDate')}")
        
        if proyecto_data.get("endDate"):
            try:
                end_date = datetime.strptime(proyecto_data.get("endDate"), "%Y-%m-%d").date()
            except ValueError:
                print(f"Error al convertir la fecha de fin: {proyecto_data.get('endDate')}")
        
        # Crear objeto Project
        project = Project(
            nombre=nombre,
            fundedAmount=funded_amount,
            startdate=start_date,
            enddate=end_date,
            papers=[paper] if paper else None
        )
        
        # Mostrar información del proyecto encontrado
        print(f"Proyecto encontrado: {project.nombre} y asociado al paper: {paper.title}")
        
        return project
        
    except Exception as e:
        print(f"Error al buscar proyecto: {e}")
        return None

def buscar_proyectos_asociados_paper(paper):
    """
    Busca todos los proyectos asociados a un paper.
    
    El proceso consta de dos pasos:
    1. Busca los IDs de proyectos asociados al paper por su título
    2. Para cada ID, obtiene los detalles completos del proyecto
    
    Args:
        paper (Paper): Objeto Paper con el título a buscar
        
    Returns:
        list: Lista de objetos Project asociados al paper
    """
    try:
        # Paso 1: Obtener IDs de proyectos asociados al paper
        proyecto_ids = buscar_proyectos_por_titulo(paper)
        
        if not proyecto_ids:
            #print(f"No se encontraron proyectos asociados al paper: {paper.title}")
            return []
        
        # Paso 2: Obtener información detallada de cada proyecto
        proyectos = []
        for proyecto_id in proyecto_ids:
            proyecto = buscar_proyecto_por_id(proyecto_id, paper)
            if proyecto:
                print(f"Proyecto encontrado: {proyecto.nombre}")
                proyecto.mostrar_info()
                proyectos.append(proyecto)
        
        # Resumen de resultados
        print(f"\nSe encontraron {len(proyectos)} de {len(proyecto_ids)} proyectos asociados al paper: {paper.title}")
        
        return proyectos
        
    except Exception as e:
        print(f"Error al buscar proyectos asociados al paper: {e}")
        return []