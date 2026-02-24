from scraper.navegador import iniciar_chrome, cerrar_chrome, check_captcha, aceptar_cookies, construir_url
from scraper.paginacion import scrapear_pagina, siguiente_pagina
from scraper.extractor import extraer_experiencias
from exportar.exportar_csv import guardar_csv
from exportar.exportar_json import guardar_json
from historial.rastreador import detectar_nuevas


def preguntar_datos():
    print("\n========================================")
    print("   InfoJobs Scraper")
    print("========================================\n")

    puesto = input("Que puesto quieres buscar? (ej: desarrollador junior): ").strip()
    if not puesto:
        puesto = "desarrollador junior"
        print(f"  Usando por defecto: {puesto}")

    ubicacion = input("En que ubicacion? (ej: españa, madrid, barcelona): ").strip()
    if not ubicacion:
        ubicacion = "españa"
        print(f"  Usando por defecto: {ubicacion}")

    print("\nCuantas paginas quieres scrapear?")
    print("  0 o enter - Todas las disponibles")
    print("  1, 2, 3... - Numero concreto")
    paginas = input("Paginas: ").strip()

    if not paginas or paginas == "0":
        paginas = 0
    elif paginas.isdigit() and int(paginas) >= 1:
        paginas = int(paginas)
    else:
        print("  Valor no valido, scrapeando todas")
        paginas = 0

    print("\nFormato de exportacion:")
    print("  1 - CSV")
    print("  2 - JSON")
    print("  3 - Ambos")
    formato = input("Elige formato (por defecto 3): ").strip()
    if formato not in ["1", "2", "3"]:
        formato = "3"

    print("\nExtraer experiencia requerida de cada oferta?")
    print("(Requiere visitar cada oferta individualmente, mas lento)")
    extraer_exp = input("s/n (por defecto n): ").strip().lower()
    extraer_exp = extraer_exp == "s"

    return puesto, ubicacion, paginas, formato, extraer_exp


def exportar_ofertas(ofertas, formato):
    if not ofertas:
        print("No se han encontrado ofertas para exportar")
        return

    if formato in ["1", "3"]:
        guardar_csv(ofertas)
    if formato in ["2", "3"]:
        guardar_json(ofertas)


def main():
    puesto, ubicacion, paginas, formato, extraer_exp = preguntar_datos()

    url = construir_url(puesto, ubicacion)
    print(f"\nURL generada: {url}")

    modo_todas = paginas == 0
    if modo_todas:
        print("Modo: scrapear TODAS las paginas disponibles")
    else:
        print(f"Modo: scrapear {paginas} paginas")

    driver = iniciar_chrome()

    try:
        driver.get(url)
        check_captcha(driver)
        aceptar_cookies(driver)

        todas_las_ofertas = []
        pagina_actual = 1

        while True:
            print(f"\n--- PAGINA {pagina_actual} ---")

            ofertas = scrapear_pagina(driver)
            todas_las_ofertas.extend(ofertas)

            print(f"Llevamos {len(todas_las_ofertas)} ofertas acumuladas")

            # si el usuario pidio un numero concreto y ya llegamos, paramos
            if not modo_todas and pagina_actual >= paginas:
                break

            # intentamos pasar a la siguiente
            if not siguiente_pagina(driver):
                print("No hay mas paginas disponibles")
                break

            pagina_actual += 1

        print(f"\nScraping completado: {len(todas_las_ofertas)} ofertas en {pagina_actual} paginas")

        # si el usuario quiere extraemos la experiencia visitando cada oferta
        if extraer_exp and todas_las_ofertas:
            extraer_experiencias(driver, todas_las_ofertas)

        # comparamos con el historico para ver cuales son nuevas
        nuevas = detectar_nuevas(todas_las_ofertas)

        # exportamos todas las ofertas encontradas
        exportar_ofertas(todas_las_ofertas, formato)

        # si hay nuevas las marcamos en consola
        if nuevas:
            print(f"\nOfertas nuevas desde la ultima ejecucion:")
            for oferta in nuevas:
                print(f"  - {oferta.titulo} ({oferta.empresa})")

        print(f"\nProceso finalizado")

    finally:
        # cerramos chrome de forma limpia
        cerrar_chrome(driver)


if __name__ == "__main__":
    main()