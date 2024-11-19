import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Función para enviar el correo
def sendmail(to_email, subject, body):
    try:
        from_email = st.secrets["FROM_EMAIL"]
        from_password = st.secrets["FROM_PASSWORD"]

        # Configuración del servidor SMTP (en este ejemplo, Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Crear la conexión SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Usar TLS para seguridad        
        server.login(from_email, from_password)  # Autenticación
    
        # Crear el mensaje
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        # Enviar el correo
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error al enviar el correo: {e}")
        return False
