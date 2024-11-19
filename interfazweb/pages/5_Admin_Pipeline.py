import streamlit as st
import subprocess
import pandas as pd
import time
import utils.utils_pipeline as up

NF_PATH = st.secrets["NF_PATH"]
NF_APP = st.secrets["NF_APP"]
NF_data_folder = st.secrets["NF_data_folder"]
NF_output_folder = st.secrets["NF_output_folder"]
NF_status_folder = st.secrets["NF_status_folder"]


# Interfaz en Streamlit
st.title("Supervisión de Procesos de Nextflow")

# Agregar un botón para detener o activar la actualización automática
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = True

if st.button("Actualizar Manualmente"):
    st.session_state.auto_refresh = False

if st.button("Habilitar Actualización Automática"):
    st.session_state.auto_refresh = True

# Actualización automática cada 30 segundos
if st.session_state.auto_refresh:
    st.markdown("### Actualización automática activa (cada 30 segundos)")
    # Agregar un temporizador visible al usuario
    time_placeholder = st.empty()
    for remaining in range(5, 0, -1):
        time_placeholder.markdown(f"Actualizando en: {remaining} segundos")
        time.sleep(1)
    st.rerun()

# Obtener los procesos de Nextflow
processes = up.get_nextflow_processes()

if processes:
    # Mostrar una tabla de procesos
    df = pd.DataFrame(processes)
    st.dataframe(df)

    options = ["Seleccione un proceso..."] + df["NAME"].tolist()
    selected_process_name = st.selectbox("Selecciona un proceso para más detalles:", options)

    if selected_process_name and selected_process_name!="Seleccione un proceso...":        
        st.query_params.jobid = selected_process_name
        if "jobid" not in st.session_state:
            st.session_state.jobid = ""
            
        st.session_state.jobid = selected_process_name

        st.switch_page("pages/4_Output.py")        
else:
    st.info("No se encontraron procesos en ejecución.")