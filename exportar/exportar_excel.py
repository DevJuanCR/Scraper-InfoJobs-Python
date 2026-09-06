import os
from configuracion import CARPETA_SALIDA
from openpyxl import Workbook
from openpyxl.styles import Font


def guardar_excel(ofertas, nombre_archivo="ofertas_infojobs.xlsx"):
    ruta = os.path.join(CARPETA_SALIDA, nombre_archivo)
    print(f"Guardando {len(ofertas)} ofertas en {ruta}...")

    try:
        os.makedirs(CARPETA_SALIDA, exist_ok=True)

        columnas = ["titulo", "empresa", "ciudad", "enlace", "salario", "contrato", "jornada", "experiencia"]

        libro = Workbook()
        hoja = libro.active
        hoja.title = "Ofertas"

        # cabecera en negrita para que se lea mejor
        hoja.append(columnas)
        for celda in hoja[1]:
            celda.font = Font(bold=True)

        for oferta in ofertas:
            datos = oferta.a_diccionario()
            hoja.append([datos[columna] for columna in columnas])

        # dejamos la primera fila fija y el ancho de columna a ojo
        hoja.freeze_panes = "A2"
        anchos = {"A": 45, "B": 30, "C": 22, "D": 55, "E": 25, "F": 18, "G": 18, "H": 22}
        for letra, ancho in anchos.items():
            hoja.column_dimensions[letra].width = ancho

        libro.save(ruta)

        print(f"Excel guardado: {ruta}")
    except Exception as e:
        print(f"Error guardando Excel: {e}")
