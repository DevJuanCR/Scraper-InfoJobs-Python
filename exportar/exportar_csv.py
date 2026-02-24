import os
import csv
from configuracion import CARPETA_SALIDA


def guardar_csv(ofertas, nombre_archivo="ofertas_infojobs.csv"):
    ruta = os.path.join(CARPETA_SALIDA, nombre_archivo)
    print(f"Guardando {len(ofertas)} ofertas en {ruta}...")

    try:
        os.makedirs(CARPETA_SALIDA, exist_ok=True)

        columnas = ["titulo", "empresa", "ciudad", "enlace", "salario", "contrato", "jornada", "experiencia"]

        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=columnas)
            writer.writeheader()
            # convertimos cada oferta a dict para escribirla
            for oferta in ofertas:
                writer.writerow(oferta.a_diccionario())

        print(f"CSV guardado: {ruta}")
    except Exception as e:
        print(f"Error guardando CSV: {e}")