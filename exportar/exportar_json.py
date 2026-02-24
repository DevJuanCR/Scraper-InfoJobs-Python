import os
import json
from configuracion import CARPETA_SALIDA


def guardar_json(ofertas, nombre_archivo="ofertas_infojobs.json"):
    ruta = os.path.join(CARPETA_SALIDA, nombre_archivo)
    print(f"Guardando {len(ofertas)} ofertas en {ruta}...")

    try:
        os.makedirs(CARPETA_SALIDA, exist_ok=True)

        # convertimos las ofertas a lista de dicts
        datos = [oferta.a_diccionario() for oferta in ofertas]

        # ensure_ascii=False para que no escape tildes y ñ
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)

        print(f"JSON guardado: {ruta}")
    except Exception as e:
        print(f"Error guardando JSON: {e}")