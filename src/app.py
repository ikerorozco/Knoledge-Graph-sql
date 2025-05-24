# app.py
import os
import streamlit as st
import streamlit.components.v1 as components
from rdflib import Graph
import pandas as pd

# vistas
from views.graph_view   import show_graph
from views.consultas_view  import show_authors_by_paper, show_paper_search
from views.map_view     import show_org_map
from views.timeline     import show_project_timeline, show_publications_by_year

st.set_page_config(page_title="Explorador KG", layout="wide")
st.title("🔍 Explorador de Knowledge Graph")

@st.cache_data
def load_graph(path="data/graphs/knowledge_graph.ttl"):
    g = Graph()
    g.parse(path, format="turtle")
    return g

g = load_graph()

page = st.sidebar.selectbox("📑 Navegación", [
    "Red Interactiva",
    "Autores por Paper",
    "Buscador de Papers",
    "Línea de Tiempo de Proyectos",
    "Mapa de Organizaciones"
])

if page == "Red Interactiva":
    show_graph(g)

elif page == "Autores por Paper":
    show_authors_by_paper(g)

elif page == "Buscador de Papers":
    show_paper_search(g)

elif page == "Línea de Tiempo de Proyectos":
    show_project_timeline(g)
    show_publications_by_year(g)

elif page == "Mapa de Organizaciones":
    show_org_map(g)


