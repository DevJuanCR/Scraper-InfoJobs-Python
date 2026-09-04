import re


def salario_a_numero(texto):
    # convertimos el texto del salario de infojobs a un numero anual aproximado
    if not texto or texto == "N/A":
        return None

    texto = texto.lower().replace(".", "")

    # cogemos todos los numeros que aparezcan (a veces viene un rango)
    numeros = re.findall(r"\d+", texto)
    if not numeros:
        return None

    # nos quedamos con el mas bajo del rango para no colar ofertas por el maximo
    minimo = min(int(n) for n in numeros)

    # si el salario es por mes o por hora lo pasamos a anual para poder comparar
    if "mes" in texto:
        minimo = minimo * 12
    elif "hora" in texto:
        minimo = minimo * 1800

    return minimo


def filtrar_por_salario(ofertas, minimo):
    # si no hay minimo devolvemos todas
    if not minimo:
        return ofertas

    filtradas = []
    for oferta in ofertas:
        salario = salario_a_numero(oferta.salario)

        # las ofertas sin salario publicado las dejamos pasar, si no perdemos casi todas
        if salario is None or salario >= minimo:
            filtradas.append(oferta)

    return filtradas
