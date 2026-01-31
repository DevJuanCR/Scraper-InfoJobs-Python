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

def es_oferta(elem):
    # funcion para filtrar si es un anuncio o una oferta real
    try:
        # si tiene clase banner, es publicidad, la ignoramos
        elem.find_element(By.CLASS_NAME, "ij-OfferList-banner")
        return False  
    except:
        pass
    
    # si tiene link en el titulo es oferta real
    try:
        elem.find_element(By.CSS_SELECTOR, "a.ij-OfferCardContent-description-title-link")
        return True
    except:
        return False

def sacar_datos(elem, driver):
    # extraemos toda la info de la tarjeta de la oferta
    try:
        # hacemos scroll hasta el elemento para asegurarnos que carga (sin esto las ofertas no se cargaran)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.5)  
        
        # extraemos el titulo y enlace de la oferta
        try:
            titulo_elem = elem.find_element(By.CSS_SELECTOR, "a.ij-OfferCardContent-description-title-link")
            titulo = titulo_elem.text.strip()
            link = titulo_elem.get_attribute("href")
        except:
            return None # si no tiene titulo no nos sirve
        
        # extraemos la empresa que ha publicado la oferta
        try:
            empresa = elem.find_element(By.CSS_SELECTOR, "a.ij-OfferCardContent-description-subtitle-link").text.strip()
        except:
            empresa = "N/A" # Si no hay empresa se pone "N/A"
        
        # extraemos la ciudad / localidad
        try:
            ciudad = elem.find_element(By.CSS_SELECTOR, "span.ij-OfferCardContent-description-list-item-truncate").text.strip()
        except:
            ciudad = "N/A" # Si no hay ciudad se pone "N/A"
            
        # devolvemos un diccionario con los datos limpios
        return {
            "titulo": titulo,
            "empresa": empresa,
            "ciudad": ciudad,
            "enlace": link
        }
    except Exception as e:
        print(f"  Error sacando datos: {e}")
        return None

if __name__ == "__main__":
    driver = iniciar_chrome() # Iniciamos chrome con iniciar_chrome()
    driver.get(URL) # Abrimos la url
    
    # Llamamos a las funciones de captcha y cookies
    check_captcha(driver)
    aceptar_cookies(driver)
    
    print("Probando extraccion de las primeras ofertas visibles...")
    
    # buscamos los elementos de la lista (las tarjetas)
    try:
        elems = driver.find_elements(By.CSS_SELECTOR, "li.ij-List-item.sui-PrimitiveLinkBox")
        
        # Probamos a sacar datos de las 3 primeras que encuentre
        for i, elem in enumerate(elems[:3]):
            if es_oferta(elem):
                datos = sacar_datos(elem, driver)
                if datos:
                    print(f"Oferta detectada: {datos['titulo']} en {datos['empresa']}")
    except Exception as e:
        print(f"Error en la prueba: {e}")

    print("Prueba finalizada. Cerrando en 5 segundos")
    time.sleep(5) # 5 segundos
    driver.quit() # Cerramos chrome