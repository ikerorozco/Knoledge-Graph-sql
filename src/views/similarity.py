import streamlit as st

def ver_papers_similares(papers):
    st.header("🔍 Buscar Papers Similares")

    # Input de búsqueda
    query = st.text_input("Buscar por título del paper:")

    # Filtrar papers por título
    if query:
        filtered_papers = [p for p in papers if query.lower() in p.title.lower()]
    else:
        filtered_papers = papers

    # Mostrar resultados
    for p in filtered_papers:
        with st.expander(f"📄 {p.title}"):
            if p.papersSimilares:
                st.markdown("**Papers similares:**")
                for sim in p.papersSimilares:
                    st.write(f"🔗 {sim.title}")
            else:
                st.markdown("🚫 Sin papers similares.")
