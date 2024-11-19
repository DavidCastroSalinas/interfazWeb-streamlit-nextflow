import streamlit as st
import subprocess
import os
import uuid
import utils.utils_mail as um
import utils.utils_pipeline as up

NF_PATH = st.secrets["NF_PATH"]
NF_APP = st.secrets["NF_APP"]
NF_data_folder = st.secrets["NF_data_folder"]
NF_output_folder = st.secrets["NF_output_folder"]
NF_status_folder = st.secrets["NF_status_folder"]


# Crear carpetas si no existen
os.makedirs(NF_data_folder, exist_ok=True)
os.makedirs(NF_output_folder, exist_ok=True)
os.makedirs(NF_status_folder, exist_ok=True)


jodID_PARAM = ""
if "jobid" in st.session_state:
    jodID_PARAM = st.session_state.jobid

if jodID_PARAM == "":
    jodID_PARAM = up.generate_unique_id()     
    st.session_state.jobid = jodID_PARAM

# Configuración inicial
st.set_page_config(page_title="InterfazWeb Pipeline", layout="wide")
col1, col2 = st.columns([3, 1]) 

with col1:    
    st.title("Pipeline Nextflow")
    st.write("A data integration with Nextflow")

with col2:    
    st.markdown("### ")
    jobID = st.text_input("🔍Job ID", value=jodID_PARAM,  placeholder="Job ID", max_chars=100, help="Enter a Job id of your run")


# Cargar archivo de entrada
uploaded_file = st.file_uploader("Load file ()", type=["csv", "txt"])


col1, col2 = st.columns([1, 1]) 

with col1:        
    st.markdown("### Job Title")
    job_title = st.text_input("Job Title (Optional)", placeholder="Short Description of the Job", max_chars=100, help="Short Description of the Job")

with col2:    
    st.markdown("###")
    email = st.text_input("Email (Optional)", placeholder="your@mail.com", max_chars=100, help="Pipeline output will sent to specified email")

# Botón para ejecutar el pipeline
if st.button("Run Pipeline"):
    if not uploaded_file:
        st.error("Please upload a file before running the pipeline.")
    elif not job_title.strip():
        st.error("The 'Job Title' field cannot be empty.")
    else:
        if uploaded_file:            
            st.success(f"Your tracking ID is: {jobID}")
            userFolder = f"{NF_PATH}{NF_data_folder}/{jobID}"
            
            os.makedirs(userFolder, exist_ok=True)
            # Guardar el archivo de entrada con el ID del usuario
            input_path = f"{userFolder}/input.txt"
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Ejecutar el pipeline en segundo plano
            st.write("Running pipeline... This may take a few minutes.")

            up.execute_pipeline(input_path, uploaded_file, job_title, email, jobID)
