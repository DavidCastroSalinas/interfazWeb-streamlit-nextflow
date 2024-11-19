import streamlit as st
import subprocess
import pandas as pd
import time
import streamlit as st
import subprocess
import os
import uuid
import utils.utils_mail as um
import utils.utils_pipeline as up

# Obtener parámetros de la URL
#if st.query_params["idjob"] == "1":        

if(st.query_params.get("idjob", None) is not None):
    idjobParam = st.query_params.get("idjob", None)
    st.session_state.jobid = idjobParam

if "jobid" not in st.session_state:
    st.session_state.jobid = ""

jobID = st.session_state.jobid

# Configuración inicial
st.set_page_config(page_title="Pipeline", layout="wide")
col1, col2 = st.columns([3, 1]) 

with col1:    
    st.title("Output Pipeline")
    st.write("A data integration platform")

with col2:    
    st.markdown("### ")
    jobID = st.text_input("🔍Job ID", value=jobID, placeholder="Job ID", max_chars=100, help="Enter a Job id of your run")


if(jobID):
    if up.carga_resultados(jobID) == True: 
        process_data = up.get_nextflow_processes(jobID)
        print(process_data)
        sessionData = process_data["SESSION ID"]

        #print(process_data)
        st.write(f"SessionData *[{sessionData}]*")

        #if st.button("Download Zip"):
        NF_PATH = st.secrets["NF_PATH"]
        NF_data_folder = st.secrets["NF_data_folder"]
        NF_output_folder = st.secrets["NF_output_folder"]
        userFolder = f"{NF_PATH}{NF_data_folder}/{jobID}"
        
        # Guardar el archivo de entrada con el ID del usuario
        

        col1, col2, col3 = st.columns([1, 1, 1]) 

        with col1:    
            st.markdown("Download the input file")
            input_path = f"{userFolder}/input.txt"
            up.downloadFile(input_path, "input.txt", "💾 Download Input", "text/plain")

        with col2:    
            st.markdown("Download the output file")
            input_path = f"{userFolder}/result1.txt"
            up.downloadFile(input_path, "result1.txt", "💾 Download Result1", "text/plain")

        with col3:    
            st.markdown("Download the reports")
            input_path = f"{userFolder}/reporte.pdf"
            up.downloadFile(input_path, "reporte.pdf", "💾 Download Graphics", "application/pdf")

        

        #NOTA: para borrar procesos <nombreproceso>	agitated_marcon -f