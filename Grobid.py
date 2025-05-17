import os
import sys
import argparse
import requests
import xml.etree.ElementTree as ET

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


# Configurar salida UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Argumentos de entrada
parser = argparse.ArgumentParser(description="Extraer metadatos desde PDFs usando GROBID.")
parser.add_argument("-i", "--input", default="data", help="Carpeta que contiene los archivos PDF.")
args = parser.parse_args()
PDF_DIRECTORY = args.input

if not os.path.exists(PDF_DIRECTORY):
    print(f"La carpeta '{PDF_DIRECTORY}' no existe.")
    exit(1)

# Endpoint de GROBID
GROBID_URL = "http://localhost:8070/api/processFulltextDocument"

# Namespaces TEI
namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}

# Funciones para extraer datos desde XML GROBID
def extract_title(root):
    el = root.find(".//tei:titleStmt/tei:title", namespaces)
    return el.text.strip() if el is not None and el.text else "Desconocido"

def autor_existe_en_openaire(nombre):
    try:
        api_url = f"https://api.openaire.eu/search/publications?author={nombre}&format=xml"
        response = requests.get(api_url, timeout=10)

        if response.status_code == 200:
            root = ET.fromstring(response.text)

            # Obtener el total de publicaciones de una forma más robusta
            total_el = root.find(".//{http://namespace.openaire.eu/oaf}total")
            if total_el is not None and total_el.text and total_el.text.isdigit():
                num_publicaciones = int(total_el.text)
            else:
                resultados = root.findall(".//{http://namespace.openaire.eu/oaf}result")
                num_publicaciones = len(resultados)

            # Obtener las organizaciones (si existen)
            resultados = root.findall(".//{http://namespace.openaire.eu/oaf}result")
            if len(resultados) > 0:
                organizaciones = set()
                for result in resultados:
                    publishers = result.findall(".//publisher")
                    if publishers:
                        org_name = publishers[0].text.strip() if publishers[0].text else "Desconocida"
                        organizaciones.add(org_name)
                        break
                return True, organizaciones, num_publicaciones
            return False, set(), 0
        else:
            print(f"  No se pudo validar el autor '{nombre}' (Error {response.status_code})")
            return False, set(), 0
    except Exception as e:
        print(f" Error al consultar OpenAIRE para '{nombre}': {e}")
        return False, set(), 0

def extract_authors(root):
    authors = []
    for author in root.findall(".//tei:author", namespaces):
        name_el = author.find(".//tei:persName", namespaces)
        if name_el is not None:
            full = " ".join(filter(None, [
                name_el.findtext("tei:forename", default="", namespaces=namespaces),
                name_el.findtext("tei:surname", default="", namespaces=namespaces)
            ])).strip()
            if full:
                authors.append(full)
    return authors

def extract_organizations(root):
    orgs = set()
    for aff in root.findall(".//tei:affiliation", namespaces):
        org_el = aff.find(".//tei:orgName", namespaces)
        if org_el is not None and org_el.text:
            orgs.add(org_el.text.strip())
    return list(orgs)

def extract_project(root):
    funders = []
    for fund in root.findall(".//tei:funding", namespaces):
        proj = fund.find(".//tei:orgName", namespaces)
        if proj is not None and proj.text:
            funders.append(proj.text.strip())
    return funders

def extract_page_count(root):
    refs = root.findall(".//tei:pb", namespaces)
    return len(refs)

def extract_acknowledgment(root):
    ack_texts = []
    for div in root.findall(".//tei:div[@type='acknowledgement']", namespaces):
        text = " ".join(p.strip() for p in div.itertext())
        if text:
            ack_texts.append(text.strip())
    return " ".join(ack_texts).strip()


# Procesar los archivos PDF
pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.lower().endswith(".pdf")]
if not pdf_files:
    print("No hay archivos PDF en la carpeta.")
    exit(1)

for pdf in pdf_files:
    print(f"\n Procesando: {pdf}")
    pdf_path = os.path.join(PDF_DIRECTORY, pdf)

    with open(pdf_path, "rb") as f:
        response = requests.post(GROBID_URL, files={"input": f}, data={"consolidate": "1"})

    if response.status_code != 200:
        print(f"    Error {response.status_code} al procesar {pdf}")
        continue

    try:
        root = ET.fromstring(response.text)
        title = extract_title(root)
        authors = extract_authors(root)
        organizations = extract_organizations(root)
        project = extract_project(root)
        page_count = extract_page_count(root)
        acknowledgment = extract_acknowledgment(root)

        # Validar autores contra OpenAIRE
        autores_validos = []
        for nombre_autor in authors:
            print(f" Validando autor: {nombre_autor}")
            es_valido, organizaciones, num_publicaciones = autor_existe_en_openaire(nombre_autor)

            if es_valido:
                print(f"  → Válido: {nombre_autor} tiene {num_publicaciones} publicación(es) en OpenAIRE.")
                organizacion_str = ", ".join(organizaciones) if organizaciones else None

                autor_obj = Author(
                    nombre=nombre_autor,
                    rdf_type="foaf:Person",
                    profesion="Investigador/a",
                    trabajos=num_publicaciones
                )

                autores_validos.append(autor_obj)
            else:
                print(f"  → No válido: {nombre_autor} no encontrado en OpenAIRE. Se descartará.")

        # Crear el objeto Paper solo con autores válidos
        paper_obj = Paper(
            title=title,
            doi="Desconocido",      # Puedes agregar la extracción de DOI si deseas
            date="Desconocida",     # También puedes extraer la fecha si lo necesitas
            idioma="Desconocido",   # Idem para el idioma
            veces_citado=None,
            paginas=page_count,
            rdf_type="bibo:AcademicArticle",
            autores=autores_validos
        )

        paper_obj.mostrar_info()

    except ET.ParseError as e:
        print(f"    Error al analizar XML: {e}")
