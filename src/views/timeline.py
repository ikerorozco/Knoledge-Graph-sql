# views/timeline.py

import streamlit as st
import pandas as pd
from datetime import datetime
from rdflib import Namespace, URIRef
from rdflib.namespace import RDF
import matplotlib.pyplot as plt

def show_project_timeline(g):
    """
    Muestra un diagrama de Gantt con cada proyecto
    y su duración entre startDate y endDate.
    """
    st.header("📅 Diagrama de Gantt de Proyectos")

    KG = Namespace("http://knowledge-graph.org/")
    DC = Namespace("http://purl.org/dc/elements/1.1/")

    rows = []
    for proj in g.subjects(RDF.type, KG.Project):
        title = g.value(proj, DC.title)
        if title is None:
            continue

        starts = list(g.objects(proj, KG.startDate))
        ends   = list(g.objects(proj, KG.endDate))
        if not starts or not ends:
            continue

        try:
            s = datetime.fromisoformat(str(starts[0]))
            e = datetime.fromisoformat(str(ends[0]))
        except ValueError:
            continue

        rows.append({
            "title": str(title),
            "start": s,
            "end": e
        })

    if not rows:
        st.write("No se encontraron proyectos con fechas completas.")
        return

    df = pd.DataFrame(rows).sort_values("start")

    fig, ax = plt.subplots(figsize=(10, len(df) * 0.5))

    for idx, row in df.iterrows():
        ax.barh(
            y=idx,
            width=(row["end"] - row["start"]).days,
            left=row["start"],
            height=0.4,
            align="center"
        )

    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df["title"], fontsize=10)
    ax.invert_yaxis()  # Primer proyecto arriba

    ax.set_xlabel("Fecha")
    ax.set_title("Timeline de Proyectos")
    fig.autofmt_xdate()

    st.pyplot(fig)


def show_publications_by_year(g):
    """
    Muestra un conteo de publicaciones por año, usando SPARQL para agrupar,
    luego lista los títulos del año seleccionado, y finalmente el gráfico de barras.
    """
    st.header("📆 Publicaciones por Año")

    # Namespaces
    KG = Namespace("http://knowledge-graph.org/")
    DC = Namespace("http://purl.org/dc/elements/1.1/")

    # Agrupa por año usando SPARQL
    query = """
    PREFIX kg: <http://knowledge-graph.org/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>

    SELECT (SUBSTR(str(?date),1,4) AS ?year) (COUNT(?paper) AS ?Publicaciones)
    WHERE {
      ?paper a kg:Paper ;
             dc:date ?date .
    }
    GROUP BY SUBSTR(str(?date),1,4)
    ORDER BY ?year
    """
    res = g.query(query)

    # DataFrame con años y conteos
    df = pd.DataFrame(res, columns=["year", "Publicaciones"])
    if df.empty:
        st.write("No se encontraron fechas de publicación.")
        return

    df["Año"] = df["year"].astype(int)
    df["Publicaciones"] = df["Publicaciones"].astype(int)
    df = df.set_index("Año")[["Publicaciones"]]

    # Selector de año para listar títulos
    st.write("#### Listado de Papers por Año")
    year_choice = st.selectbox("Selecciona un año:", df.index.tolist())

    # SPARQL para recuperar títulos de ese año
    q_titles = f'''
    PREFIX kg: <http://knowledge-graph.org/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>

    SELECT ?title WHERE {{
      ?paper a kg:Paper ;
             dc:date ?date ;
             dc:title ?title .
      FILTER(STRSTARTS(str(?date), "{year_choice}-"))
    }}
    ORDER BY ?title
    '''
    titles = [str(r.title) for r in g.query(q_titles)]

    if titles:
        for t in titles:
            st.write(f"- {t}")
    else:
        st.write(f"No hay papers listados para el año {year_choice}.")

    # El gráfico de barras
    st.write("#### Gráfico de barras")
    st.bar_chart(df)


