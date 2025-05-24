# views/map_view.py

import streamlit as st
import pandas as pd
import requests
from rdflib import Namespace
from rdflib.namespace import RDF, FOAF
import pydeck as pdk

def show_org_map(g):
    """
    Muestra un mapa de organizaciones, 
    extrayendo country codes y nombres vía SPARQL,
    y geolocalizando con restcountries.com.
    """
    st.header("🗺️ Mapa de Organizaciones por País")

    KG = Namespace("http://knowledge-graph.org/")

    q = """
    PREFIX kg:   <http://knowledge-graph.org/>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>

    SELECT ?orgName ?code WHERE {
      ?org a kg:Organization ;
           foaf:name ?orgName ;
           kg:location ?code .
    }
    """
    res = g.query(q)

    records = []
    for orgName, code in res:
        cc = str(code)
        try:
            r = requests.get(f"https://restcountries.com/v3.1/alpha/{cc}", timeout=5)
            r.raise_for_status()
            data = r.json()[0]["latlng"]    # [lat, lon]
            records.append({
                "Organization": str(orgName),
                "lat":  data[0],
                "lon":  data[1]
            })
        except Exception:
            continue

    if not records:
        st.write("No se geocodificaron organizaciones (¿códigos inválidos?).")
        return

    df = pd.DataFrame(records)
    st.dataframe(df[["Organization","lat","lon"]])

    # Pinta el mapa con pydeck para tener tooltips
    midpoint = (df["lat"].mean(), df["lon"].mean())
    layer = pdk.Layer(
        "ScatterplotLayer", df,
        get_position=["lon","lat"],
        get_fill_color=[255, 0, 0, 100],  
        get_radius=150000,
        pickable=True,
        auto_highlight=True
    )
    tooltip = {"html": "<b>Organization</b>: {Organization}"}

    deck = pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=midpoint[0], longitude=midpoint[1], zoom=2
        ),
        layers=[layer],
        tooltip=tooltip
    )
    st.pydeck_chart(deck)
