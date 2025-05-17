import requests
import xml.etree.ElementTree as ET
from models.base_models import Paper, Author

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
            autores=autores
        )

        print("\n--- Resultado de la búsqueda ---")
        paper.mostrar_info()
        print("--- Fin del resultado ---\n")
        return paper

    except ET.ParseError as e:
        print(f"Error al parsear XML: {e}")
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