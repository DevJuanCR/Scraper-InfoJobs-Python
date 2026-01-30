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

if __name__ == "__main__":
    driver = iniciar_chrome() # Iniciamos chrome con iniciar_chrome()
    driver.get(URL) # Abrimos la url
    print("Navegador abierto. Cerrando en 5 segundos")
    time.sleep(5) # 5 segundos
    driver.quit() # Cerramos chrome