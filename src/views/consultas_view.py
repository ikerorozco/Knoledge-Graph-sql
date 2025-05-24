import streamlit as st
import pandas as pd
from rdflib import Namespace, URIRef
from rdflib.namespace import RDF, FOAF

def show_authors_by_paper(g):
    st.header("✍️ Autores por Paper")

    KG = Namespace("http://knowledge-graph.org/")
    DC = Namespace("http://purl.org/dc/elements/1.1/")

    q = """
    PREFIX kg:   <http://knowledge-graph.org/>
    PREFIX dc:   <http://purl.org/dc/elements/1.1/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?paper ?paperTitle ?authorName WHERE {
      ?paper a kg:Paper ;
             dc:title ?paperTitle ;
             kg:hasAuthor ?author .
      ?author foaf:name ?authorName .
    }
    ORDER BY ?paperTitle ?authorName
    """
    res = g.query(q)
    df = pd.DataFrame(res, columns=["paperURI","paperTitle","authorName"])
    if df.empty:
        st.write("No hay datos.")
        return

    grouped = df.groupby("paperTitle")["authorName"].apply(list).to_dict()

    choice = st.selectbox("Selecciona un paper:", list(grouped.keys()))
    st.write("**Autores:**")
    for a in grouped[choice]:
        st.write(f"- {a}")

def show_paper_search(g):
    """
    Permite buscar papers por palabra clave dentro de sus títulos.
    """
    st.header("🔎 Buscador de Papers por palabra clave")

    keyword = st.text_input("Escribe una palabra clave para buscar en títulos:")

    if not keyword:
        st.write("⌨️ Ingresa al menos una palabra para empezar la búsqueda.")
        return

    low = keyword.lower().replace('"', '\\"')

    KG = Namespace("http://knowledge-graph.org/")
    DC = Namespace("http://purl.org/dc/elements/1.1/")

    query = f"""
    PREFIX kg: <http://knowledge-graph.org/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>

    SELECT ?title WHERE {{
      ?paper a kg:Paper ;
             dc:title ?title .
      FILTER(CONTAINS(LCASE(str(?title)), "{low}"))
    }}
    ORDER BY ?title
    """

    results = g.query(query)

    df = pd.DataFrame(results, columns=["Título"])
    if df.empty:
        st.warning(f"No se encontraron papers que contengan “{keyword}”.")
    else:
        st.success(f"Se encontraron {len(df)} papers:")
        st.dataframe(df)

