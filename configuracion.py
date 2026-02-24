# url base de infojobs, luego le añadimos el puesto y la ubicacion
URL_BASE = "https://www.infojobs.net/ofertas-trabajo"

# selectores css y xpath para encontrar elementos en la pagina
SELECTORES = {
    # captcha
    "captcha_boton": "geetest_radar_tip",
    "captcha_superado": "//a[@data-e2e='candidate-login']",

    # cookies
    "cookies_boton": "didomi-notice-agree-button",

    # ofertas (css para la tarjeta)
    "lista_ofertas": "li.ij-List-item.sui-PrimitiveLinkBox",
    "oferta_titulo": "a.ij-OfferCardContent-description-title-link",
    "oferta_empresa": "a.ij-OfferCardContent-description-subtitle-link",
    "oferta_ciudad": "span.ij-OfferCardContent-description-list-item-truncate",
    "oferta_banner": "ij-OfferList-banner",

    # detalles de la tarjeta (xpath relativo al elemento oferta)
    "oferta_contrato": "./div/div[2]/div/ul[2]/li[1]",
    "oferta_jornada": "./div/div[2]/div/ul[2]/li[2]",
    "oferta_salario": "./div/div[2]/div/ul[2]/li[3]/span",

    # experiencia (varios xpath porque el dom cambia entre ofertas)
    "oferta_experiencia": [
        "//*[@id='app']/div[2]/div/main/section[1]/article/div[2]/div[3]/div[1]/div[2]/div[1]/p",
        "//*[@id='app']/div[2]/div[1]/main/section[1]/article/div/div[3]/div[1]/div[2]/div[1]/p",
        "//*[@id='app']/div[2]/div/main/section[1]/article/div/div[3]/div[1]/div[2]/div[1]/p",
        "//section[1]/article//div[3]/div[1]/div[2]/div[1]/p",
    ],

    # paginacion
    "boton_siguiente": "//button[contains(., 'Siguiente')] | //li[contains(@class, 'next')]//a",
}

# tiempos de espera en segundos
TIEMPOS = {
    "captcha_check": 5,
    "captcha_manual": 120,
    "cookies": 10,
    "carga_ofertas": 15,
    "entre_paginas": 3,
    "tras_cookies": 2,
    "scroll_carga": 0.5,
    "boton_siguiente": 3,
    "carga_experiencia": 5,
    "entre_ofertas_min": 1,
    "entre_ofertas_max": 3,
}

# configuracion del scroll
SCROLL_PX = 400

# carpeta donde se guardan los csv, json e historico
CARPETA_SALIDA = "salida"