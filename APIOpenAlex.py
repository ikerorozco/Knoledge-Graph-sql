import requests

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
        if not self.flagstart_date: print("   start_date no encontrada.")

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
    def __init__(self, nombre, rdf_type, profesion, trabajos):
        self.nombre = nombre
        self.rdf_type = rdf_type
        self.profesion = profesion
        self.trabajos = trabajos

        # Banderas: True si el campo fue encontrado, False si no
        self.flagRdfType = rdf_type is not None
        self.flagNombre = nombre is not None
        self.flagProfesion = profesion is not None
        self.flagTrabajos = trabajos is not None

    def mostrar_info(self):
        print(" Información del Autor:")
        print(f"  Nombre         : {self.nombre}")
        print(f"  RDF Type       : {self.rdf_type}")
        print(f"  Profesión      : {self.profesion}")
        print(f"  Trabajos       : {self.trabajos}")
        
        print("\n Campos faltantes:")
        if not self.flagNombre: print("   Nombre no encontrado.")
        if not self.flagTrabajos: print("   Trabajos no encontrados.")
        if not self.flagProfesion: print("   Profesion no encontrada.")
        if not self.flagRdfType: print("   RDF Type no encontrado.")


class Paper:
    def __init__(self, title, doi, date, idioma, veces_citado, paginas, rdf_type):
        self.title = title
        self.doi = doi
        self.date = date
        self.idioma = idioma
        self.veces_citado = veces_citado
        self.paginas = paginas
        self.rdf_type = rdf_type

        # Banderas: True si el campo fue encontrado, False si no
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


def buscar_por_titulo_openalex(titulo):
    try:
        # Codificar el título para que sea seguro en una URL
        titulo_codificado = requests.utils.quote(titulo)
        
        # Construir la URL de la API
        api_url = f"https://api.openalex.org/works?filter=title.search:{titulo_codificado}"

        # Realizar la consulta HTTP
        response = requests.get(api_url, timeout=10)

        if response.status_code == 200:
            datos = response.json()
            resultados = datos.get("results", [])

            if resultados:
                for i, resultado in enumerate(resultados, start=1):
                    titulo_encontrado = resultado.get("title")
                    doi = resultado.get("doi")
                    fecha = resultado.get("publication_date")
                    idioma = resultado.get("language")
                    veces_citado = resultado.get("cited_by_count")
                    paginas = resultado.get("biblio", {}).get("pages")
                    rdf_type = resultado.get("type")
                    
                    # Crear el objeto Paper
                    paper = Paper(
                        title=titulo_encontrado,
                        doi=doi,
                        date=fecha,
                        idioma=idioma,
                        veces_citado=veces_citado,
                        paginas=paginas,
                        rdf_type=rdf_type
                    )

                    # Extraer información sobre los autores
                    autores = resultado.get("authorships", [])
                    for i, autor in enumerate(autores, start=1):
    # Extraer datos del autor
                        autor_nombre = autor.get("author", {}).get("display_name", "Nombre no disponible")
                        autor_rdf_type = autor.get("author", {}).get("type")
                        autor_profesion = autor.get("author", {}).get("affiliation", {}).get("name", "No especificado")
                        autor_trabajos = autor.get("author", {}).get("works_count", 0)

                        author = Author(
                            nombre=autor_nombre,
                            rdf_type=autor_rdf_type,
                            profesion=autor_profesion,
                            trabajos=autor_trabajos
                        )
                        print(f"\nAutor {i}:")
                        author.mostrar_info()

    # Aquí dentro, para cada autor, obtener las instituciones
                        instituciones = autor.get("institutions", [])
                        for inst in instituciones:
                            org_nombre = inst.get("display_name")
                            org_lugar = inst.get("country_code")
                            org_rdf_type = inst.get("type")
                            org_trabajos = inst.get("works_count", 0)
                            org_links = inst.get("id")

                            organizacion = Organizacion(
                                nombre=org_nombre,
                                lugar=org_lugar,
                                rdftype=org_rdf_type,
                                trabajos=org_trabajos,
                                links=org_links
                )
                            organizacion.mostrar_info()

                    
                    # Mostrar la información del Paper
                    print(f"Resultado {i}:")
                    paper.mostrar_info()
                    return paper  # Opcional: puedes devolver el objeto Paper para usarlo con OpenAIRE

            else:
                print("No se encontraron resultados en OpenAlex.")
        else:
            print(f"Error al consultar OpenAlex (Error {response.status_code})")

    except Exception as e:
        print(f"Error al consultar OpenAlex para '{titulo}': {e}")

# Ejemplo de uso
titulo = "Quality over Quantity: Boosting Data Efficiency Through Ensembled Multimodal Data Curation"
paper = buscar_por_titulo_openalex(titulo)
