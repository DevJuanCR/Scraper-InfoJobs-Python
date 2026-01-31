import time
import random
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
            EC.presence_of_element_located((By.XPATH, "//a[@data-e2e='candidate-login']")) # XPATH del boton "Acceso Candidatos"
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

def scrapear_ofertas(driver):
    # aqui hacemos scroll lento y vamos cogiendo ir cogiendo ofertas
    print("Empezando scraping con scroll lento...")
    
    ofertas_ya_sacadas = set()  # usamos un set para guardar los links y no repetir ofertas
    todas_ofertas = [] # lista final donde guardaremos los datos
    
    # esperamos a que carguen las primeras ofertas
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ij-List-item.sui-PrimitiveLinkBox")) # Class que tienen las ofertas
        )
        print("Primeras ofertas cargadas")
        time.sleep(2)
    except:
        print("No se cargaron ofertas :/")
        return []
    
    # volvemos arriba del todo por si acaso
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    
    altura = 0
    altura_total = driver.execute_script("return document.body.scrollHeight") # altura total de la pagina
    scroll_px = 400  # bajamos 400px cada vez
    veces_sin_ofertas = 0 # contador para saber cuando parar
    
    print(f"Altura pagina inicial: {altura_total}px")
    
    contador_scrolls = 0
    
    # bucle para ir bajando mientras no lleguemos al final
    while altura < altura_total:
        contador_scrolls += 1
        altura += scroll_px
        driver.execute_script(f"window.scrollTo(0, {altura});") # hacemos scroll
        
        # esperar random para parecer humano (entre 1 y 2 segundos)
        time.sleep(random.uniform(1, 2))
        
        # buscamos las ofertas que esten visibles ahora
        elems = driver.find_elements(By.CSS_SELECTOR, "li.ij-List-item.sui-PrimitiveLinkBox")
        
        nuevas = 0
        for elem in elems:
            if not es_oferta(elem):
                continue # si es publicidad pasamos
            
            try:
                # sacamos el link primero para ver si ya la tenemos
                link = elem.find_element(By.CSS_SELECTOR, "a.ij-OfferCardContent-description-title-link").get_attribute("href")
                
                if link in ofertas_ya_sacadas:
                    continue  # si ya esta en el set, saltamos a la siguiente
                
                # si es nueva, sacamos los datos
                datos = sacar_datos(elem, driver)
                
                if datos:
                    todas_ofertas.append(datos)
                    ofertas_ya_sacadas.add(link) # la añadimos al set de procesadas
                    nuevas += 1
                    print(f"  -> Nueva oferta: {datos['titulo']} ({datos['empresa']})")
            except:
                continue
        
        # logica para saber si estamos atascados o hemos terminado
        if nuevas > 0:
            print(f"Scroll {contador_scrolls}: Encontradas {nuevas} ofertas nuevas")
            veces_sin_ofertas = 0 # reseteamos el contador
        else:
            veces_sin_ofertas += 1
            print(f"Scroll {contador_scrolls}: 0 nuevas...")
        
        # actualizamos la altura total por si ha crecido la pagina (carga dinamica)
        nueva_altura_total = driver.execute_script("return document.body.scrollHeight")
        if nueva_altura_total > altura_total:
            altura_total = nueva_altura_total
        
        # si llevamos 5 scrolls seguidos sin encontrar nada nuevo, paramos
        if veces_sin_ofertas >= 5:
            print(f"Parece que no hay mas ofertas")
            break
    
    print(f"Scraping terminado. Total encontradas: {len(todas_ofertas)}")
    return todas_ofertas

if __name__ == "__main__":
    driver = iniciar_chrome() # Iniciamos chrome con iniciar_chrome()
    driver.get(URL) # Abrimos la url
    
    # Llamamos a las funciones de captcha y cookies
    check_captcha(driver)
    aceptar_cookies(driver)
    
    # Probamos la funcion completa de scraping
    ofertas = scrapear_ofertas(driver)
    
    print(f"Hecho! Se han extraido {len(ofertas)} ofertas en total.")
    driver.quit() # Cerramos chrome