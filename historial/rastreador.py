import os
import json
from datetime import datetime
from configuracion import CARPETA_SALIDA

CARPETA_HISTORICO = os.path.join(CARPETA_SALIDA, "historico")
ARCHIVO_HISTORICO = os.path.join(CARPETA_HISTORICO, "historico.json")


def cargar_historico():
    # cargamos el historico anterior si existe
    if not os.path.exists(ARCHIVO_HISTORICO):
        return {}

    try:
        with open(ARCHIVO_HISTORICO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except Exception as e:
        print(f"Error cargando historico, empezamos de cero: {e}")
        return {}


def guardar_historico(historico):
    try:
        os.makedirs(CARPETA_HISTORICO, exist_ok=True)

        with open(ARCHIVO_HISTORICO, "w", encoding="utf-8") as archivo:
            json.dump(historico, archivo, ensure_ascii=False, indent=2)

        print(f"Historico actualizado: {ARCHIVO_HISTORICO}")
    except Exception as e:
        print(f"Error guardando historico: {e}")


def detectar_nuevas(ofertas):
    historico = cargar_historico()
    nuevas = []
    repetidas = 0
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")

    for oferta in ofertas:
        # usamos el enlace como id unico de cada oferta
        if oferta.enlace not in historico:
            nuevas.append(oferta)
            # guardamos la oferta con la fecha en que la vimos por primera vez
            historico[oferta.enlace] = {
                "titulo": oferta.titulo,
                "empresa": oferta.empresa,
                "ciudad": oferta.ciudad,
                "primera_vez": fecha_actual,
            }
        else:
            repetidas += 1

    guardar_historico(historico)

    print(f"\n--- Resumen historico ---")
    print(f"Ofertas encontradas: {len(ofertas)}")
    print(f"Ofertas nuevas: {len(nuevas)}")
    print(f"Ofertas que ya teniamos: {repetidas}")
    print(f"Total en historico: {len(historico)}")

    return nuevas