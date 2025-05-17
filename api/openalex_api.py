import requests
from models.base_models import Paper, Author, Organizacion

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
                    # Extraer información básica del paper
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
                        # Extraer datos del autor
                        autor_nombre = autor_data.get("author", {}).get("display_name", "Nombre no disponible")
                        autor_rdf_type = autor_data.get("author", {}).get("type")
                        autor_profesion = autor_data.get("author", {}).get("affiliation", {}).get("name", "No especificado")
                        autor_trabajos = autor_data.get("author", {}).get("works_count", 0)

                        # Crear objeto Autor
                        autor = Author(
                            nombre=autor_nombre,
                            rdf_type=autor_rdf_type,
                            profesion=autor_profesion,
                            trabajos=autor_trabajos
                        )
                        autores.append(autor)

                        # Procesar instituciones del autor
                        for inst_data in autor_data.get("institutions", []):
                            org_nombre = inst_data.get("display_name")
                            org_lugar = inst_data.get("country_code")
                            org_rdf_type = inst_data.get("type")
                            org_trabajos = inst_data.get("works_count", 0)
                            org_links = inst_data.get("id")

                            organizacion = Organizacion(
                                nombre=org_nombre,
                                lugar=org_lugar,
                                rdftype=org_rdf_type,
                                trabajos=org_trabajos,
                                links=org_links
                            )
                            print(f"\nInstitución asociada al autor {autor_nombre}:")
                            organizacion.mostrar_info()

                    # Crear el objeto Paper
                    paper = Paper(
                        title=titulo_encontrado,
                        doi=doi,
                        date=fecha,
                        idioma=idioma,
                        veces_citado=veces_citado,
                        paginas=paginas,
                        rdf_type=rdf_type,
                        autores=autores
                    )

                    # Mostrar la información del Paper
                    print(f"\nResultado {i}:")
                    paper.mostrar_info()
                    return paper

            else:
                print("No se encontraron resultados en OpenAlex.")
                return None
        else:
            print(f"Error al consultar OpenAlex (Error {response.status_code})")
            return None

    except Exception as e:
        print(f"Error al consultar OpenAlex para '{titulo}': {e}")
        return None 