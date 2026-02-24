import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configuracion import SELECTORES, TIEMPOS, SCROLL_PX
from scraper.extractor import es_oferta, extraer_oferta


def scroll_completo(driver):
    # bajamos poco a poco para que cargue todo el contenido dinamico
    altura = 0
    altura_total = driver.execute_script("return document.body.scrollHeight")

    while altura < altura_total:
        altura += SCROLL_PX
        driver.execute_script(f"window.scrollTo(0, {altura});")
        time.sleep(TIEMPOS["scroll_carga"])
        # actualizamos por si la pagina ha crecido con carga dinamica
        altura_total = driver.execute_script("return document.body.scrollHeight")

    # volvemos arriba
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)


def scrapear_pagina(driver):
    print("Analizando pagina actual...")
    ofertas_pagina = []
    enlaces_procesados = set()

    # primero hacemos scroll completo para forzar la carga
    scroll_completo(driver)

    try:
        # esperamos a que haya ofertas en el dom
        WebDriverWait(driver, TIEMPOS["carga_ofertas"]).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, SELECTORES["lista_ofertas"]))
        )
    except:
        print("No se cargaron ofertas en esta pagina")
        return ofertas_pagina

    elementos = driver.find_elements(By.CSS_SELECTOR, SELECTORES["lista_ofertas"])
    print(f"Elementos encontrados: {len(elementos)}")

    for elemento in elementos:
        if not es_oferta(elemento):
            continue

        oferta = extraer_oferta(elemento, driver)
        if oferta and oferta.enlace not in enlaces_procesados:
            ofertas_pagina.append(oferta)
            enlaces_procesados.add(oferta.enlace)
            print(f"  Oferta: {oferta.titulo} ({oferta.empresa})")

    print(f"Ofertas extraidas en esta pagina: {len(ofertas_pagina)}")
    return ofertas_pagina


def siguiente_pagina(driver):
    try:
        print("Buscando boton de siguiente pagina...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        boton = WebDriverWait(driver, TIEMPOS["boton_siguiente"]).until(
            EC.element_to_be_clickable((By.XPATH, SELECTORES["boton_siguiente"]))
        )

        driver.execute_script("arguments[0].click();", boton)
        print("Cambiando de pagina...")
        # espera random para parecer humano
        time.sleep(TIEMPOS["entre_paginas"] + random.uniform(0, 1))
        return True
    except:
        print("No se encontro el boton siguiente o es la ultima pagina")
        return False