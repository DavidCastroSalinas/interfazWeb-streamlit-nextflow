import matplotlib.pyplot as plt
from fpdf import FPDF
import sys

# Leer argumentos desde la línea de comandos
param1 = sys.argv[1]
param2 = sys.argv[2]

# Crear un gráfico con Matplotlib
def crear_grafico(name_graph_file="grafico.png"):
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 15, 25, 30]

    plt.figure(figsize=(6, 4))
    plt.plot(x, y, marker="o", label="Datos")
    plt.title("Ejemplo de gráfico")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid()

    # Guardar el gráfico como imagen
    plt.savefig(name_graph_file, bbox_inches="tight")
    plt.close()

# Crear un PDF con el gráfico
def crear_pdf(path_file="grafico.pdf", name_graph_file = "grafico.png"):

    crear_grafico(name_graph_file)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Agregar título
    pdf.cell(200, 10, txt="Gráfico generado en PDF", ln=True, align="C")

    # Insertar el gráfico como imagen
    pdf.image(name_graph_file, x=10, y=30, w=190)  # Ajusta x, y y w según sea necesario

    # Guardar el PDF
    pdf.output(path_file)
    print(f"PDF generado: {path_file}")

crear_pdf(param1, param2)