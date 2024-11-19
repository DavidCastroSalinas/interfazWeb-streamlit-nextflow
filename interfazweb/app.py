import streamlit as st

if "jobid" not in st.session_state:
    st.session_state.jobid = ""


# Configuración de la app
st.title("Interfaz Nextflow")
st.write("")

st.markdown("""
Webserver details

    The interface developed on Python 3.9 using Streamlit 1.31.0;
    This website does not use any cookies.

    # Pipeline overview
"""
)
