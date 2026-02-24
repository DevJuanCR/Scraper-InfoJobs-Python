import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configuracion import SELECTORES, TIEMPOS


def iniciar_chrome():
    print("Abriendo Chrome...")
    # sin version_main para que detecte solo la version instalada
    driver = uc.Chrome()
    return driver


def cerrar_chrome(driver):
    try:
        driver.quit()
    except OSError:
        pass
    # parcheamos __del__ para que no intente cerrar otra vez en windows
    try:
        driver.__class__.__del__ = lambda self: None
    except:
        pass


def check_captcha(driver):
    print("Comprobando captcha...")
    try:
        WebDriverWait(driver, TIEMPOS["captcha_check"]).until(
            EC.presence_of_element_located((By.CLASS_NAME, SELECTORES["captcha_boton"]))
        )
        print("CAPTCHA DETECTADO. Completalo manualmente por favor...")

        # damos tiempo para resolverlo a mano
        WebDriverWait(driver, TIEMPOS["captcha_manual"]).until(
            EC.presence_of_element_located((By.XPATH, SELECTORES["captcha_superado"]))
        )
        print("Captcha superado, continuamos")
    except:
        print("No hay captcha")


def aceptar_cookies(driver):
    try:
        print("Buscando banner de cookies...")
        boton = WebDriverWait(driver, TIEMPOS["cookies"]).until(
            EC.element_to_be_clickable((By.ID, SELECTORES["cookies_boton"]))
        )
        boton.click()
        print("Cookies aceptadas")
        time.sleep(TIEMPOS["tras_cookies"])
    except:
        print("No aparecio el banner de cookies")


def construir_url(puesto, ubicacion):
    # formateamos el puesto y ubicacion para meterlos en la url
    puesto_formateado = puesto.strip().replace(" ", "-").lower()
    ubicacion_formateada = ubicacion.strip().replace(" ", "-").lower()
    from configuracion import URL_BASE
    return f"{URL_BASE}/{puesto_formateado}/{ubicacion_formateada}"