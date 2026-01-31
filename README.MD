# InfoJobs Web Scraper

Herramienta de automatización desarrollada en Python para la extracción de ofertas de empleo del portal InfoJobs. Este proyecto utiliza Selenium y undetected-chromedriver para simular navegación humana, permitiendo la recolección de datos sin utilizar la API oficial.

El script está diseñado específicamente para buscar ofertas de "Desarrollador Junior" en España, aunque el código es adaptable a otros criterios de búsqueda.

## Características Técnicas

* **Evasión de detección:** Implementación de `undetected-chromedriver` para evitar bloqueos por huella digital del navegador (fingerprinting).
* **Carga dinámica (AJAX):** Algoritmo de scroll automático diseñado para activar la carga de nuevas ofertas en el DOM.
* **Gestión de Cookies:** Detección y aceptación automática del banner de consentimiento GDPR mediante selectores CSS/XPATH.
* **Sistema deteccion de Captcha:** Detección de Captchas "Geetest". El script pausa la ejecución y espera resolución manual si es necesario, continuando el flujo automáticamente después.
* **Navegación y Paginación:** Permite al usuario definir el número de páginas a procesar mediante input en consola.
* **Persistencia de datos:** Exportación automática de resultados a formato CSV estructurado (UTF-8).
* **Comportamiento humano:** Tiempos de espera aleatorios (`random.uniform`) entre acciones para reducir el riesgo de bloqueo de IP.

## Requisitos

* Python 3.11.9 o superior
* Google Chrome instalado (si no tienes la versión 145 ajustalo en el codigo a tu versión)

## Instalación

1. Clonar el repositorio:

git clone [https://github.com/DevJuanCR/Scraper-InfoJobs-Python.git](https://github.com/DevJuanCR/Scraper-InfoJobs-Python.git)
cd Scraper-InfoJobs-Python

2. Instalar dependencias:

pip install -r requirements.txt

## Uso

Ejecutar el script principal desde la terminal:

python main.py

El programa solicitará el número de páginas a escanear.

Al finalizar, se generará un archivo ofertas_infojobs.csv en el directorio raíz con las siguientes columnas:

**Título de la oferta**

**Empresa**

**Ciudad**

**Enlace directo**

## Notas
Este script depende de la estructura HTML actual de InfoJobs. Si el portal actualiza sus clases CSS o la estructura del DOM, es posible que sea necesario actualizar los selectores en el código fuente.

## Aviso Legal
Este software ha sido desarrollado con fines puramente educativos para demostrar habilidades de programación y web scraping ético. No está afiliado ni respaldado por InfoJobs. El uso de scripts automatizados debe realizarse de manera responsable.