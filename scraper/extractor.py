import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configuracion import SELECTORES, TIEMPOS
from modelos.oferta import Oferta


def es_oferta(elemento):
    # si tiene clase banner es publicidad
    try:
        elemento.find_element(By.CLASS_NAME, SELECTORES["oferta_banner"])
        return False
    except:
        pass

    # si tiene link en el titulo es oferta real
    try:
        elemento.find_element(By.CSS_SELECTOR, SELECTORES["oferta_titulo"])
        return True
    except:
        return False


def extraer_texto(elemento, selector, por_defecto="N/A"):
    # sacamos el texto de un elemento con css selector
    try:
        return elemento.find_element(By.CSS_SELECTOR, selector).text.strip()
    except:
        return por_defecto


def extraer_texto_xpath(elemento, xpath, por_defecto="N/A"):
    # sacamos el texto de un elemento con xpath relativo
    try:
        return elemento.find_element(By.XPATH, xpath).text.strip()
    except:
        return por_defecto


def extraer_atributo(elemento, selector, atributo, por_defecto="N/A"):
    # sacamos un atributo (href, src, etc) de un elemento
    try:
        return elemento.find_element(By.CSS_SELECTOR, selector).get_attribute(atributo)
    except:
        return por_defecto


def buscar_experiencia(driver):
    # probamos varios xpath porque infojobs cambia la estructura entre ofertas
    for xpath in SELECTORES["oferta_experiencia"]:
        try:
            elem = driver.find_element(By.XPATH, xpath)
            texto = elem.text.strip()
            if texto:
                return texto
        except:
            continue
    return "N/A"


def extraer_oferta(elemento, driver):
    try:
        # scroll hasta el elemento para que cargue
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        time.sleep(0.5)

        titulo = extraer_texto(elemento, SELECTORES["oferta_titulo"])
        enlace = extraer_atributo(elemento, SELECTORES["oferta_titulo"], "href")

        # si no tiene titulo o enlace no nos sirve
        if titulo == "N/A" or enlace == "N/A":
            return None

        empresa = extraer_texto(elemento, SELECTORES["oferta_empresa"])
        ciudad = extraer_texto(elemento, SELECTORES["oferta_ciudad"])

        # sacamos contrato, jornada y salario con xpath relativo a la tarjeta
        contrato = extraer_texto_xpath(elemento, SELECTORES["oferta_contrato"])
        jornada = extraer_texto_xpath(elemento, SELECTORES["oferta_jornada"])
        salario = extraer_texto_xpath(elemento, SELECTORES["oferta_salario"])

        return Oferta(
            titulo=titulo,
            empresa=empresa,
            ciudad=ciudad,
            enlace=enlace,
            salario=salario,
            contrato=contrato,
            jornada=jornada,
            experiencia="N/A",
        )
    except Exception as e:
        print(f"  Error extrayendo oferta: {e}")
        return None


def extraer_experiencias(driver, ofertas):
    # visitamos cada oferta para sacar la experiencia requerida
    total = len(ofertas)
    print(f"\nExtrayendo experiencia de {total} ofertas...")
    print("(esto puede tardar un rato)\n")

    for i, oferta in enumerate(ofertas, 1):
        titulo_corto = oferta.titulo[:50] + "..." if len(oferta.titulo) > 50 else oferta.titulo
        print(f"  [{i}/{total}] {titulo_corto}", end="", flush=True)

        try:
            driver.get(oferta.enlace)

            # esperamos a que cargue la pagina de la oferta
            WebDriverWait(driver, TIEMPOS["carga_experiencia"]).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            time.sleep(1)

            oferta.experiencia = buscar_experiencia(driver)
            print(f" -> {oferta.experiencia}")

        except:
            print(" -> No disponible")

        # espera random para parecer humano
        time.sleep(random.uniform(TIEMPOS["entre_ofertas_min"], TIEMPOS["entre_ofertas_max"]))

    print("\nExperiencias extraidas")