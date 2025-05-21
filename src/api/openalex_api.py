import requests
from models.paper import Paper
from models.author import Author
from models.organization import Organization

def buscar_por_titulo_openalex(titulo_o_paper):
    """
    Si recibe un string, busca y retorna un Paper.
    Si recibe un objeto Paper, lo complementa con la información de OpenAlex y lo retorna.
    Además, complementa la información de cada autor y organización usando OpenAlex.
    """
    # Determinar si el argumento es un objeto Paper o un string
    if isinstance(titulo_o_paper, Paper):
        paper_obj = titulo_o_paper
        titulo = paper_obj.title
    else:
        paper_obj = None
        titulo = titulo_o_paper

    try:
        titulo_codificado = requests.utils.quote(titulo)
        api_url = f"https://api.openalex.org/works?filter=title.search:{titulo_codificado}"
        response = requests.get(api_url, timeout=10)

        if response.status_code == 200:
            datos = response.json()
            resultados = datos.get("results", [])

            if resultados:
                resultado = resultados[0]  # Tomar el primer resultado relevante

                # Extraer información básica
                titulo_encontrado = resultado.get("title")
                doi = resultado.get("doi")
                fecha = resultado.get("publication_date")
                idioma = resultado.get("language")
                veces_citado = resultado.get("cited_by_count")
                paginas = resultado.get("biblio", {}).get("pages")
                rdf_type = resultado.get("type")

                # Crear lista de autores
                autores = []
                for autor_data in resultado.get("authorships", []):
                    autor_nombre = autor_data.get("author", {}).get("display_name", "Nombre no disponible")
                    autor_rdf_type = autor_data.get("author", {}).get("type")
                    autor_profesion = autor_data.get("author", {}).get("affiliation", {}).get("name", "No especificado")
                    autor_trabajos = autor_data.get("author", {}).get("works_count", 0)
                    autor = Author(
                        nombre=autor_nombre,
                        rdf_type=autor_rdf_type,
                        profesion=autor_profesion,
                        trabajos=autor_trabajos
                    )
                    # Complementar información del autor usando OpenAlex
                    autor = complementar_autor_con_openalex(autor)
                    autores.append(autor)

                # Procesar instituciones del autor (puedes mejorar esto para evitar duplicados)
                organizaciones = []
                for autor_data in resultado.get("authorships", []):
                    for inst_data in autor_data.get("institutions", []):
                        org_nombre = inst_data.get("display_name")
                        org_lugar = inst_data.get("country_code")
                        org_rdf_type = inst_data.get("type")
                        org_trabajos = inst_data.get("works_count", 0)
                        org_links = inst_data.get("id")
                        organizacion = Organization(
                            nombre=org_nombre,
                            lugar=org_lugar,
                            rdftype=org_rdf_type,
                            trabajos=org_trabajos,
                            links=org_links
                        )
                        # Complementar información de la organización usando OpenAlex
                        organizacion = complementar_organizacion_con_openalex(organizacion)
                        organizaciones.append(organizacion)

                # Si se recibió un objeto Paper, complementar sus atributos
                if paper_obj:
                    if not paper_obj.doi: paper_obj.doi = doi
                    if not paper_obj.date: paper_obj.date = fecha
                    if not paper_obj.idioma: paper_obj.idioma = idioma
                    if not paper_obj.veces_citado: paper_obj.veces_citado = veces_citado
                    if not paper_obj.paginas: paper_obj.paginas = paginas
                    if not paper_obj.rdf_type: paper_obj.rdf_type = rdf_type
                    if not paper_obj.autores or len(paper_obj.autores) == 0:
                        paper_obj.autores = autores
                    else:
                        # Complementar cada autor existente
                        for i, autor in enumerate(paper_obj.autores):
                            paper_obj.autores[i] = complementar_autor_con_openalex(autor)
                    if not paper_obj.organization or len(paper_obj.organization) == 0:
                        paper_obj.organization = organizaciones
                    else:
                        # Complementar cada organización existente
                        for i, org in enumerate(paper_obj.organization):
                            paper_obj.organization[i] = complementar_organizacion_con_openalex(org)
                    if not paper_obj.title: paper_obj.title = titulo_encontrado
                    print("\nPaper complementado con OpenAlex:")
                    paper_obj.mostrar_info()
                    return paper_obj
                else:
                    # Si no, crear un nuevo objeto Paper
                    paper = Paper(
                        title=titulo_encontrado,
                        doi=doi,
                        date=fecha,
                        idioma=idioma,
                        veces_citado=veces_citado,
                        paginas=paginas,
                        rdf_type=rdf_type,
                        autores=autores,
                        organization=organizaciones
                    )
                    print(f"\nResultado OpenAlex:")
                    paper.mostrar_info()
                    return paper

            else:
                print("No se encontraron resultados en OpenAlex.")
                return paper_obj if paper_obj else None
        else:
            print(f"Error al consultar OpenAlex (Error {response.status_code})")
            return paper_obj if paper_obj else None

    except Exception as e:
        print(f"Error al consultar OpenAlex para '{titulo}': {e}")
        return paper_obj if paper_obj else None


def complementar_autor_con_openalex(autor):
    """
    Busca información adicional del autor en OpenAlex y complementa el objeto Author.
    """
    try:
        nombre_codificado = requests.utils.quote(autor.nombre)
        api_url = f"https://api.openalex.org/authors?filter=display_name.search:{nombre_codificado}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            datos = response.json()
            resultados = datos.get("results", [])
            if resultados:
                resultado = resultados[0]
                # Solo actualiza si el campo está vacío o es None
                if not autor.rdf_type: autor.rdf_type = resultado.get("type")
                if not autor.trabajos: autor.trabajos = resultado.get("works_count")
                if not autor.profesion: autor.profesion = resultado.get("last_known_institution", {}).get("display_name")
                # Puedes agregar más campos según tu modelo Author
        return autor
    except Exception as e:
        print(f"Error al complementar autor '{autor.nombre}' en OpenAlex: {e}")
        return autor

def complementar_organizacion_con_openalex(organizacion):
    """
    Busca información adicional de la organización en OpenAlex y complementa el objeto Organization.
    """
    try:
        if not organizacion.nombre:
            return organizacion
        nombre_codificado = requests.utils.quote(organizacion.nombre)
        api_url = f"https://api.openalex.org/institutions?filter=display_name.search:{nombre_codificado}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            datos = response.json()
            resultados = datos.get("results", [])
            if resultados:
                resultado = resultados[0]
                # Solo actualiza si el campo está vacío o es None
                if not organizacion.rdftype: organizacion.rdftype = resultado.get("type")
                if not organizacion.lugar: organizacion.lugar = resultado.get("country_code")
                if not organizacion.trabajos: organizacion.trabajos = resultado.get("works_count")
                if not organizacion.links: organizacion.links = resultado.get("id")
                # Puedes agregar más campos según tu modelo Organization
        return organizacion
    except Exception as e:
        print(f"Error al complementar organización '{organizacion.nombre}' en OpenAlex: {e}")
        return organizacion
    

