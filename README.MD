# InfoJobs Scraper

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4-43B02A?logo=selenium&logoColor=white)
![Chrome](https://img.shields.io/badge/Chrome-autodetect-4285F4?logo=googlechrome&logoColor=white)
![CSV](https://img.shields.io/badge/Export-CSV-217346?logo=microsoftexcel&logoColor=white)
![JSON](https://img.shields.io/badge/Export-JSON-000000?logo=json&logoColor=white)

Herramienta de web scraping desarrollada en Python que extrae ofertas de empleo de [InfoJobs](https://www.infojobs.net) de forma automatizada. Busca cualquier puesto en cualquier ubicación de España, exporta los datos a CSV/JSON y detecta ofertas nuevas entre ejecuciones.

![Dashboard](docs/demo.gif)

## Características

| Característica | Descripción |
|---|---|
| **Búsqueda personalizada** | Puesto y ubicación configurables desde consola |
| **Paginación automática** | Detecta y recorre todas las páginas disponibles |
| **Evasión de detección** | ``undetected-chromedriver`` para evitar bloqueos por fingerprinting |
| **Autodetección de Chrome** | Detecta automáticamente la versión de Chrome instalada |
| **Gestión de cookies** | Acepta el banner GDPR de forma automática |
| **Detección de captcha** | Pausa y espera resolución manual si aparece un captcha |
| **Exportación flexible** | CSV, JSON o ambos formatos |
| **Historial** | Detecta ofertas nuevas comparando con ejecuciones anteriores |
| **Comportamiento humano** | Tiempos aleatorios entre acciones para evitar bloqueos |

## Datos extraídos por oferta

| Campo | Fuente | Descripción |
|---|---|---|
| Título | Listado | Nombre del puesto |
| Empresa | Listado | Empresa que publica la oferta |
| Ciudad | Listado | Ubicación del puesto |
| Salario | Listado | Rango salarial si está disponible |
| Contrato | Listado | Tipo de contrato (indefinido, temporal...) |
| Jornada | Listado | Tipo de jornada (completa, parcial...) |
| Experiencia | Detalle | Experiencia requerida (requiere visitar cada oferta) |
| Enlace | Listado | URL directa a la oferta |

## Estructura del proyecto

```bash
Scraper-InfoJobs-Python/
├── main.py                  # Punto de entrada con menu interactivo
├── configuracion.py         # Selectores, tiempos y configuracion centralizada
├── scraper/
│   ├── navegador.py         # Chrome, captcha y cookies
│   ├── extractor.py         # Extraccion de datos de cada oferta
│   └── paginacion.py        # Scroll y cambio de pagina
├── modelos/
│   └── oferta.py            # Dataclass que representa una oferta
├── exportar/
│   ├── exportar_csv.py      # Exportacion a CSV
│   └── exportar_json.py     # Exportacion a JSON
├── historial/
│   └── rastreador.py        # Historico y deteccion de ofertas nuevas
├── salida/                  # Archivos generados (CSV, JSON, historico)
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.11 o superior
- Google Chrome instalado (cualquier versión, se detecta automáticamente)

## Instalación

```bash
git clone https://github.com/DevJuanCR/Scraper-InfoJobs-Python.git
cd Scraper-InfoJobs-Python
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

El programa te pedirá:

1. **Puesto a buscar** — desarrollador junior, data engineer, diseñador gráfico...
2. **Ubicación** — españa, madrid, barcelona...
3. **Número de páginas** — un número concreto o todas las disponibles
4. **Formato de exportación** — CSV, JSON o ambos
5. **Extraer experiencia** — visita cada oferta para sacar la experiencia requerida (opcional, más lento)

Los resultados se guardan en la carpeta ``salida/``.

### Ejemplo de ejecución

```bash
========================================
   InfoJobs Scraper
========================================

Que puesto quieres buscar? (ej: desarrollador junior): desarrollador junior
En que ubicacion? (ej: españa, madrid, barcelona): madrid
Cuantas paginas quieres scrapear? (0 = todas): 0
Formato de exportacion: 3
Extraer experiencia requerida? s/n: s

--- PAGINA 1 ---
  Oferta: Desarrollador/a Junior Salesforce (Grupo Hasten)
  Oferta: Programador/a Full Stack Junior (prodereg)
  ...

--- PAGINA 2 ---
  Oferta: Desarrollador Java Junior (NTT Data)
  ...

Scraping completado: 147 ofertas en 8 paginas

Extrayendo experiencia de 147 ofertas...
  [1/147] Desarrollador/a Junior Salesforce -> Al menos 1 año
  [2/147] Programador/a Full Stack Junior -> No requerida
  ...

--- Resumen historico ---
Ofertas encontradas: 147
Ofertas nuevas: 23
Ofertas que ya teniamos: 124
Total en historico: 312

Proceso finalizado
```

### Ejemplo de salida JSON

```json
[
  {
    "titulo": "Desarrollador/a Junior Salesforce",
    "empresa": "Grupo Hasten",
    "ciudad": "Madrid",
    "enlace": "https://www.infojobs.net/...",
    "salario": "18.000€ - 22.000€ Bruto/año",
    "contrato": "Indefinido",
    "jornada": "Completa",
    "experiencia": "Al menos 1 año"
  }
]
```

## Sistema de historial

El scraper guarda un registro en ``salida/historico/historico.json`` con todas las ofertas vistas y la fecha en que aparecieron por primera vez. En cada ejecución compara las ofertas actuales con el historial y te muestra cuáles son nuevas. Útil para ejecutarlo periódicamente y no perderte ninguna vacante.

## Configuración

Todos los selectores CSS/XPath, tiempos de espera y configuración del scroll están centralizados en ``configuracion.py``. Si InfoJobs actualiza su estructura HTML, solo hay que modificar los selectores en ese archivo.

## Notas

- Si aparece un captcha, el script te avisa y espera hasta 2 minutos para que lo resuelvas manualmente.
- La extracción de experiencia requiere visitar cada oferta individualmente, lo que aumenta el tiempo de ejecución y el riesgo de captcha.
- Los selectores dependen de la estructura HTML actual de InfoJobs. Si el portal cambia su diseño, puede ser necesario actualizarlos en ``configuracion.py``.

## Aviso legal

Este software ha sido desarrollado con fines educativos para demostrar habilidades de programación y web scraping. No está afiliado ni respaldado por InfoJobs. El uso de scripts automatizados debe realizarse de manera responsable y respetando los términos de servicio del sitio web.