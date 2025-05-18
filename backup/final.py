import os
import uuid
import sys
import requests
import xml.etree.ElementTree as ET
import argparse
import matplotlib.pyplot as plt
import networkx as nx
from transformers import pipeline
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD, FOAF

# Configurar salida UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Argumentos
parser = argparse.ArgumentParser(description="Extrae y visualiza RDF desde PDFs.")
parser.add_argument("-i", "--input", default="data", help="Carpeta de PDFs.")
args = parser.parse_args()
PDF_DIRECTORY = args.input

if not os.path.exists(PDF_DIRECTORY):
    print(f"La carpeta '{PDF_DIRECTORY}' no existe.")
    exit(1)

# URL del servicio GROBID
GROBID_URL = "http://localhost:8070/api/processFulltextDocument"

# Namespaces RDF
FIN = Namespace("http://www.owl-ontologies.com/financiamiento#")
DC = Namespace("http://purl.org/dc/elements/1.1/")
VC = Namespace("http://www.owl-ontologies.com/vecesCitado#")
IDIOMA = Namespace("http://www.owl-ontologies.com/idioma#")

# Crear grafo RDF
g = Graph()
g.bind("fin", FIN)
g.bind("dc", DC)
g.bind("vc", VC)
g.bind("idioma", IDIOMA)
g.bind("foaf", FOAF)

# Namespaces XML
namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}

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

def extract_metadata(xml_text):
    try:
        root = ET.fromstring(xml_text)
        authors = []
        for author in root.findall(".//tei:author", namespaces):
            name_el = author.find(".//tei:persName", namespaces)
            if name_el is not None:
                full = " ".join(filter(None, [
                    name_el.findtext("tei:forename", default="", namespaces=namespaces),
                    name_el.findtext("tei:surname", default="", namespaces=namespaces)
                ])).strip()
                if full and full not in authors:
                    authors.append(full)
            if len(authors) == 5:
                break
        return authors
    except ET.ParseError:
        return []

def extract_title(xml_text):
    try:
        root = ET.fromstring(xml_text)
        title_el = root.find(".//tei:titleStmt/tei:title", namespaces)
        title = title_el.text.strip() if title_el is not None and title_el.text else "Desconocido"
        return title
    except ET.ParseError:
        return "Desconocido"

# Procesar PDFs
pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.lower().endswith(".pdf")]
if not pdf_files:
    print("No hay archivos PDF en la carpeta.")
    exit(1)

for pdf in pdf_files:
    print(f"\nProcesando: {pdf}")
    pdf_path = os.path.join(PDF_DIRECTORY, pdf)
    with open(pdf_path, "rb") as f:
        response = requests.post(GROBID_URL, files={"input": f}, data={"consolidate": "1"})

    if response.status_code != 200:
        print(f"   Error {response.status_code} al procesar {pdf}")
        continue

    xml_text = response.text
    authors = extract_metadata(xml_text)
    title = extract_title(xml_text)

    # Crear URI del paper
    paper_id = str(uuid.uuid4())
    paper_uri = URIRef(f"http://example.org/paper/{paper_id}")

    # Aquí se agrega el título al grafo y se imprime en consola
    g.add((paper_uri, RDF.type, FIN.Paper))
    g.add((paper_uri, DC.title, Literal(title, lang="es")))

    print(f"Título del PDF: {title}")  # Muestra el título en la pantalla

    # Procesar autores y organizaciones
    for name in authors:
        existe, organizaciones, num_publicaciones = autor_existe_en_openaire(name)

        if existe:
            author_uri = URIRef(f"http://example.org/author/{name.replace(' ', '_')}")
            g.add((paper_uri, FIN.hasAuthor, author_uri))
            g.add((author_uri, RDF.type, FIN.Author))
            g.add((author_uri, DC.title, Literal(name)))
            g.add((author_uri, FIN.publicationCount, Literal(num_publicaciones, datatype=XSD.integer)))

            if organizaciones:
                org = next(iter(organizaciones))  # Tomamos solo la primera organización
                g.add((author_uri, FIN.worksFor, Literal(org)))
                print(f"        -> Organización: {org}")
            print(f"       Agregado: {name}")
        else:
            print(f"       Descarta: {name} (no encontrado en OpenAIRE)")

# Guardar el grafo RDF
output_file = "grafo_autores_simple.ttl"
g.serialize(output_file, format="turtle")
print(f"\nGrafo RDF guardado en '{output_file}'")

# Visualizar el grafo RDF
print("\n🔍 Visualizando grafo...")

g = Graph()
g.parse(output_file, format="turtle")

# Crear grafo con NetworkX
G = nx.DiGraph()
edge_labels = {}

# Simplificar URIs para las etiquetas
def simplify(uri):
    uri = str(uri)
    if "#" in uri:
        return uri.split("#")[-1]
    elif "/" in uri:
        return uri.split("/")[-1]
    return uri

# Diccionario de colores para los nodos
node_colors = {}

# Crear un diccionario para mapear URI del paper al título
paper_titles = {}

for s, p, o in g:
    if str(p) == str(DC.title):
        paper_titles[str(s)] = str(o)

# Construir nodos y relaciones usando títulos legibles
for s, p, o in g:
    subj_label = paper_titles.get(str(s), simplify(s))
    obj_label = paper_titles.get(str(o), simplify(o))
    pred_label = simplify(p)

    # Agregar colores a los nodos
    if "author" in str(s):  # Si el sujeto es un autor
        node_colors[subj_label] = 'lightblue'  # Azul para autores
    elif "publisher" in str(o):  # Si el objeto es una organización
        node_colors[obj_label] = 'red'  # Rojo para organizaciones
    elif "Paper" in str(s):  # Si el sujeto es un Paper
        node_colors[subj_label] = 'green'  # Verde para papers
    
    if "author" in str(o):  # Si el objeto es un autor
        node_colors[obj_label] = 'lightblue'  # Azul para autores
    elif "publisher" in str(s):  # Si el sujeto es una organización
        node_colors[subj_label] = 'red'  # Rojo para organizaciones
    elif "Paper" in str(o):  # Si el objeto es un Paper
        node_colors[obj_label] = 'green'  # Verde para papers

    G.add_edge(subj_label, obj_label)
    edge_labels[(subj_label, obj_label)] = pred_label

# Posiciones para graficar
pos = nx.spring_layout(G, k=0.8, iterations=100)

# Dibujar
plt.figure(figsize=(16, 12))
node_color_list = [node_colors.get(node, 'lightgray') for node in G.nodes()]

nx.draw(G, pos, with_labels=True,
        node_size=2000,
        node_color=node_color_list,  # Asignamos los colores de los nodos
        font_size=9,
        font_weight='bold',
        edge_color='gray',
        arrowsize=15)

# Dibujar las etiquetas de las aristas
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                             font_size=8, font_color="red")

# Título y presentación
plt.title("Grafo RDF simplificado (Autores, Organizaciones y Papers)", fontsize=14)
plt.tight_layout()
plt.show()
