import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.infojobs.net/ofertas-trabajo/desarrollador-junior/espana" # URL que vamos a scrapear en este caso InfoJobs 

def iniciar_chrome():
    print("Abriendo Chrome...")
    # Ajusta version_main a tu versión de Chrome si es necesario
    driver = uc.Chrome(version_main=114) # En este caso tengo la version 114 de chrome
    return driver

def check_captcha(driver):
    # comprobamos si nos ha saltado el captcha de seguridad
    print("Comprobando captcha...")
    try:
        # esperamos maximo 5 seg a ver si sale el captcha
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "geetest_radar_tip"))
        )
        print("CAPTCHA DETECTADO. Completalo manualmente por favor...")
        
        # si sale, damos 120 segundos (2 min) para resolverlo a mano
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//a[@data-e2e='candidate-login']")) # XPATH del boton "Acceso Candidatos" (He utilizado este xpath ya que es un boton que se carga cuando estamos en la pagina deseada)
        )
        print("Captcha superado, continuamos")
    except:
        print("No hay captcha") # si salta la excepcion es que no habia captcha

def aceptar_cookies(driver):
    # gestionamos el popup de cookies de InfoJobs
    try:
        print("Buscando banner de cookies...")
        # esperamos a que el boton de aceptar sea clickeable con un timeout de 10 segundos
        boton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")) # buscamos por id el boton de aceptar cookies
        )
        boton.click() # hacemos click al boton de aceptar
        print("Cookies aceptadas")
        time.sleep(2) # esperamos 2 segundos a que se cierre
    except:
        print("No aparecio el banner de cookies") # puede que ya esten aceptadas

if __name__ == "__main__":
    driver = iniciar_chrome() # Iniciamos chrome con iniciar_chrome()
    driver.get(URL) # Abrimos la url
    
    # Llamamos a las funciones de captcha y cookies
    check_captcha(driver)
    aceptar_cookies(driver)
    
    print("Pagina lista. Cerrando en 5 segundos")
    time.sleep(5) # 5 segundos
    driver.quit() # Cerramos chrome