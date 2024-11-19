import streamlit as st
import subprocess
import pandas as pd
import utils.utils_mail as um
import json
import datetime
import hashlib

NF_PATH = st.secrets["NF_PATH"]
NF_APP = st.secrets["NF_APP"]
NF_data_folder = st.secrets["NF_data_folder"]
NF_output_folder = st.secrets["NF_output_folder"]
NF_status_folder = st.secrets["NF_status_folder"]
URL_APP = st.secrets["URL_APP"]


def generate_unique_id():
    # Obtener la fecha y hora actual
    now = datetime.datetime.now()
    # Convertirla en un string único
    timestamp = now.strftime("%Y%m%d%H%M%S%f")  # AñoMesDíaHoraMinutoSegundoMicrosegundo
    # Crear un hash y reducirlo a 8 caracteres
    unique_id = 'MH-'+hashlib.md5(timestamp.encode()).hexdigest()[:8]
    return unique_id

# Función para obtener los procesos de Nextflow en ejecución
def get_nextflow_processes(nameProcess=""):
    try:
        print(f"{NF_PATH + 'nextflow'}")
        result = subprocess.run(["nextflow", "log"], cwd=NF_PATH, capture_output=True, text=True)
        if result.returncode != 0:
            st.error("Error al ejecutar el comando `nextflow log`.")
            st.text(result.stderr)
            return []

        # Parsear la salida del comando
        processes = []
        for line in result.stdout.splitlines():
            if line.strip() and not line.startswith("TIMESTAMP"):  # Ignorar encabezado
                fields = line.split()
                #print(fields)

                record = {
                    "NAME": fields[3],
                    "STATUS": fields[4],
                    "DURATION": fields[2],
                    "DATE": fields[0],
                    "TIME": fields[1],                    
                    #"REVISION": fields[5],
                    "SESSION ID": fields[6],
                    "COMMAND": fields[7],
                    #"ID2": fields[8],
                    #"COMMAND": fields[9],
                }

                if(nameProcess != "" and nameProcess == fields[3]):
                    return record

                processes.append(record)
                #print(processes)
        return processes
    except Exception as e:
        st.error(f"Error al obtener los procesos de Nextflow: {e}")
        return []


def carga_resultados(selected_process_name):

    NF_PATH = st.secrets["NF_PATH"]
    NF_APP = st.secrets["NF_APP"]
    NF_data_folder = st.secrets["NF_data_folder"]
    NF_output_folder = st.secrets["NF_output_folder"]
    NF_status_folder = st.secrets["NF_status_folder"]

    if selected_process_name:
        st.subheader(f"Details [{selected_process_name}]")
        try:

            fields = ["name","status",  "duration", "start", "memory"]

            args = ['nextflow', 'log', selected_process_name, '-f'] + [",".join(fields)] 
            result2 = subprocess.run(args, cwd=NF_PATH, capture_output=True, text=True)
            
            if result2.returncode != 0:
                st.error("[Error] IDJOB not found")
                #st.text(result2.stderr)
                return False
            else: 
                # Parsear la salida del comando
                processes = []
                #print(result2.stdout)
                for line in result2.stdout.splitlines():
                    if line.strip() and not line.startswith("TIMESTAMP2"):  # Ignorar encabezado
                        fields = line.split()
                        #print(fields)
                        print(fields[0])
                        processes.append({
                            "NAME": fields[0] ,
                            "STATUS": fields[1],
                            "DURATION": fields[2],
                            "DATE": fields[3],
                            "TIME": fields[4],
                        })       

                df2 = pd.DataFrame(processes)
                st.dataframe(df2)
                return True
        except Exception as e:
            st.error(f"Error durante la ejecución: {e}")    
            return False







# Función para ejecutar el pipeline de Nextflow con un ID de usuario
def run_pipeline(jobID, input_file):
    NF_output_folder = st.secrets["NF_output_folder"]
    NF_status_folder = st.secrets["NF_status_folder"]

    userFolder = f"{NF_PATH}{NF_data_folder}/{jobID}"

    output_path = f"{userFolder}/result.txt"
    status_path = f"{userFolder}/status.json"

    # Actualizar el estado a "En progreso"
    with open(status_path, "w") as f:
        json.dump({"status": "En progreso"}, f)

    # Ejecutar el pipeline de Nextflow
    args = ['nextflow', 
            "run", "main.nf",
            "-name", jobID,
            "--input_file", input_file,
            "--output_dir", userFolder
            ]

    result = subprocess.run(args, cwd=NF_PATH, capture_output=True, text=True)
    print(args)

    # Actualizar el estado basado en el resultado de la ejecución
    if result.returncode == 0:
        with open(status_path, "w") as f:
            json.dump({"status": "Completo", "output": output_path}, f)
            return True
    else:
        with open(status_path, "w") as f:
            json.dump({"status": "Error", "error": result.stderr}, f)
            return False



            



# Función para simular la ejecución del pipeline
def execute_pipeline(input_path, file, job_title, email, jobID):
    if( run_pipeline(jobID, input_path) == True ):
        st.write("### Pipeline resume:")
        st.write(f"📄 File uploaded: {file.name if file else 'not uploaded'}")
        st.write(f"🏷️ Job Title: {job_title}")
        st.write(f"📧 Email: {email if email else 'No email'}")
        st.write(f"Link to the output page will expire in 7 days: {URL_APP}/Output?idjob={jobID}")
        st.success("Pipeline executed successfully!")
        
        if email:
            subject = f"[Mobhunter] Pipeline MobHunter ({jobID})"
            body = f"JobTitle: {job_title}  Filename:{file.name} jobID:{jobID}   Please go to: {URL_APP}/Output?idjob={jobID}"
            if um.sendmail(email, subject, body):
                st.success("Mail sent successfully!")            


def downloadFile(file_path, file_name="archivo", buttonText="Download File", mimeFormat = "text/plain"):
    # Verificar si el archivo existe
    try:
        # Leer el contenido del archivo
        with open(file_path, "rb") as file:
            file_content = file.read()
        
        # Título de la aplicación
        #st.title(buttonText)

        # Botón de descarga
        st.download_button(
            label=buttonText,
            data=file_content,
            mime=mimeFormat
        )

    except FileNotFoundError:
        st.error(f"The file at path '{file_path}' does not exist.")                