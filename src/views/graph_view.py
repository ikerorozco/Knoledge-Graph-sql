import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
from rdflib import Namespace, URIRef
from rdflib.namespace import RDF, FOAF

def show_graph(g):
    """
    Muestra una visualización interactiva del grafo RDF 'g' en Streamlit,
    distinguiendo Papers, Authors y Organizations con colores y formas,
    y etiquetando las aristas con sus predicados.
    """
    st.header("🌐 Red Interactiva del Knowledge Graph")

    KG = Namespace("http://knowledge-graph.org/")
    DC = Namespace("http://purl.org/dc/elements/1.1/")

    # Estilos visuales por tipo
    TYPE_STYLE = {
        str(KG.Paper)       : {"color": "lightgreen", "shape": "box"},
        str(KG.Author)      : {"color": "skyblue",   "shape": "ellipse"},
        str(KG.Organization): {"color": "orange",    "shape": "triangle"},
        str(KG.Project)     : {"color": "lightcoral", "shape": "diamond"}
    }
    HUMAN_TYPE = {
        str(KG.Paper)       : "Paper",
        str(KG.Author)      : "Author",
        str(KG.Organization): "Organization",
        str(KG.Project)     : "Project"
    }

    # Construye un grafo NetworkX con el predicado como atributo
    Gnx = nx.Graph()
    for s, p, o in g:
        sid, oid = str(s), str(o)
        Gnx.add_node(sid)
        Gnx.add_node(oid)
        Gnx.add_edge(sid, oid, predicate=str(p))

    # Filtra solo nodos de los tres tipos principales
    allowed_nodes = set()
    for type_uri in TYPE_STYLE:
        for subj in g.subjects(RDF.type, URIRef(type_uri)):
            allowed_nodes.add(str(subj))

    # Crea la red PyVis
    net = Network(
        height="700px", width="100%",
        bgcolor="#ffffff", font_color="black",
        notebook=False
    )
    net.force_atlas_2based()

    # Añade nodos con estilo y tooltip
    for node in allowed_nodes:
        uri = URIRef(node)

        # Determina tipo humano
        tipos = [str(t) for t in g.objects(uri, RDF.type)]
        matched = next((t for t in tipos if t in HUMAN_TYPE), None)
        human_type = HUMAN_TYPE.get(matched, "Unknown")

        # Nombre legible
        if human_type == "Paper":
            title = g.value(uri, DC.title)
            human_name = str(title).strip() if title else node.split("/")[-1]
        else:
            name = g.value(uri, FOAF.name)
            human_name = str(name).strip() if name else node.split("/")[-1]

        # Estilo
        style = TYPE_STYLE.get(matched, {"color": "lightgray", "shape": "dot"})

        # Tooltip
        tooltip = f"<b>{human_name}</b><br/><i>{human_type}</i>"

        net.add_node(
            node,
            label=human_name,
            title=tooltip,
            color=style["color"],
            shape=style["shape"]
        )

    # Añade aristas etiquetadas
    for u, v, data in Gnx.edges(data=True):
        if u in allowed_nodes and v in allowed_nodes:
            raw = data.get("predicate", "")
            pred = raw.split("#")[-1] if "#" in raw else raw.split("/")[-1]
            net.add_edge(u, v, label=pred, title=pred)

    # Guarda y embebe
    tmpfile = "tmp_kg.html"
    net.save_graph(tmpfile)
    html = open(tmpfile, "r", encoding="utf-8").read()
    components.html(html, height=700, scrolling=True)
