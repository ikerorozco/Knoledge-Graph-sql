import requests
import xml.etree.ElementTree as ET

class Proyecto:
    def __init__(self, nombre, financiamiento, rdftype, cordinador,start_date):
        self.nombre = nombre
        self.financiamiento = financiamiento
        self.rdftype = rdftype
        self.cordinador = cordinador
        self.start_date = start_date

        self.flagNombre = nombre is not None
        self.flagFinanciamiento = financiamiento is not None
        self.flagRdfType = rdftype is not None
        self.flagcordinador = cordinador is not None
        self.flagstart_date = start_date is not None

    def mostrar_info(self):
        print(" Información de la organizacion:")
        print(f"  Nombre         : {self.nombre}")
        print(f"  financiamiento       : {self.financiamiento or 'No disponible'}")
        print(f"  rdftype      : {self.rdftype or 'No disponible'}")
        print(f"  cordinador       : {self.cordinador or 'No disponible'}")
        print(f"  start_date       : {self.start_date or 'No disponible'}")
        
        print("\n Campos faltantes:")
        if not self.flagNombre: print("   Nombre no encontrado.")
        if not self.flagFinanciamiento: print("   financiamiento no encontrado.")
        if not self.flagcordinador: print("   cordinador no encontrado.")
        if not self.flagRdfType: print("   RDF Type no encontrado.")
        if not self.flagstart_date: print("   start_date no encontrad.")

class Organizacion:
    def __init__(self, nombre, lugar, rdftype, trabajos,links):
        self.nombre = nombre
        self.lugar = lugar
        self.rdftype = rdftype
        self.trabajos = trabajos
        self.links = links

        self.flagNombre = nombre is not None
        self.flagLugar = lugar is not None
        self.flagRdfType = rdftype is not None
        self.flagTrabajos = trabajos is not None
        self.flagLinks = links is not None

    def mostrar_info(self):
        print(" Información de la organizacion:")
        print(f"  Nombre         : {self.nombre}")
        print(f"  lugar       : {self.lugar or 'No disponible'}")
        print(f"  rdftype      : {self.rdftype or 'No disponible'}")
        print(f"  Trabajos       : {self.trabajos or 'No disponible'}")
        print(f"  links       : {self.links or 'No disponible'}")
        
        print("\n Campos faltantes:")
        if not self.flagNombre: print("   Nombre no encontrado.")
        if not self.flagTrabajos: print("   Trabajos no encontrados.")
        if not self.lugar: print("   lugar no encontrado.")
        if not self.flagRdfType: print("   RDF Type no encontrado.")
        if not self.links: print("   links no encontrados.")

class Author:
    def __init__(self, nombre, rdf_type=None, profesion=None, trabajos=None):
        self.nombre = nombre
        self.rdf_type = rdf_type
        self.profesion = profesion
        self.trabajos = trabajos

        self.flagRdfType = rdf_type is not None
        self.flagNombre = nombre is not None
        self.flagProfesion = profesion is not None
        self.flagTrabajos = trabajos is not None

    def mostrar_info(self):
        print(" Información del Autor:")
        print(f"  Nombre         : {self.nombre}")
        print(f"  RDF Type       : {self.rdf_type or 'No disponible'}")
        print(f"  Profesión      : {self.profesion or 'No disponible'}")
        print(f"  Trabajos       : {self.trabajos or 'No disponible'}")
        
        print("\n Campos faltantes:")
        if not self.flagNombre: print("   Nombre no encontrado.")
        if not self.flagTrabajos: print("   Trabajos no encontrados.")
        if not self.flagProfesion: print("   Profesión no encontrada.")
        if not self.flagRdfType: print("   RDF Type no encontrado.")

class Paper:
    def __init__(self, title, doi, date, idioma, veces_citado, paginas, rdf_type, autores):
        self.title = title
        self.doi = doi
        self.date = date
        self.idioma = idioma
        self.veces_citado = veces_citado
        self.paginas = paginas
        self.rdf_type = rdf_type
        self.autores = autores

        self.flagTitle = title is not None
        self.flagDoi = doi is not None
        self.flagDate = date is not None
        self.flagIdioma = idioma is not None
        self.flagVecesCitado = veces_citado is not None
        self.flagPaginas = paginas is not None
        self.flagRdfType = rdf_type is not None

    def mostrar_info(self):
        print(" Información del Paper:")
        print(f"  Título         : {self.title}")
        print(f"  DOI            : {self.doi}")
        print(f"  Fecha          : {self.date}")
        print(f"  Idioma         : {self.idioma}")
        print(f"  Veces citado   : {self.veces_citado}")
        print(f"  Páginas        : {self.paginas}")
        print(f"  RDF Type       : {self.rdf_type}")
        
        print("\n Campos faltantes:")
        if not self.flagTitle: print("   Título no encontrado.")
        if not self.flagDoi: print("   DOI no encontrado.")
        if not self.flagDate: print("   Fecha no encontrada.")
        if not self.flagIdioma: print("   Idioma no encontrado.")
        if not self.flagVecesCitado: print("   Veces citado no encontrado.")
        if not self.flagPaginas: print("   Páginas no encontradas.")
        if not self.flagRdfType: print("   RDF Type no encontrado.")
        print("\n")

        print(" Autores:")
        for autor in self.autores:
            autor.mostrar_info()
            print("\n")

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

    except ET.ParseError as e:
        print(f"Error al parsear XML: {e}")

def buscar_por_titulo(titulo):
    try:
        print(f"\n Buscando en OpenAIRE: {titulo}\n")
        api_url = f"https://api.openaire.eu/search/publications?title={titulo}&format=xml"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            parsear_xml_openaire(response.text)
        else:
            print(f"Error al consultar OpenAIRE (Error {response.status_code})")
    except Exception as e:
        print(f"Error al consultar OpenAIRE para '{titulo}': {e}")

# Ejecutar una búsqueda de prueba
titulo = "Quality over Quantity: Boosting Data Efficiency Through Ensembled Multimodal Data Curation"
buscar_por_titulo(titulo)
