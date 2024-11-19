# interfazWeb-streamlit-nextflow

considere utilizar el archivo secrets

cree una carpeta dentro de la carpeta de de STREAMLIT llamada .streamlit/ y dentro de ella cree un archivo llamado secrets.homl
dentro coloque lo siguinte:

# secrets.toml
URL_APP = "http://localhost:8501"
FROM_EMAIL = "mi@gmail.com"
FROM_PASSWORD = "" #password de aplicación de windows
FROM_CLAVE = ""
API_KEY = "api_key_secreta"
DB_HOST = "localhost"
DB_USER = "user"
DB_PASSWORD = "password"
NF_PATH = "/home/dabits/mobhunter/nextflow/" #personalice esta ruta
NF_APP = "main.nf"
NF_data_folder = "data"
NF_output_folder = "data/output"
NF_status_folder = "data/status"


