ULTIMO_TAG_ABIERTO = -1
NO_EXISTE = ""
CARACTER_APERTURA_TAG = "<"
CARACTER_BARRA_CIERRE_TAG = "/"
CARACTER_CIERRE_TAG = "</"

"""
// Pre: -

// Post: Devuelve True si linea empieza con CARACTER_APERTURA_TAG e inmediatamente no le sigue un CARACTER_BARRA_CIERRE_TAG.
//       False en cualquier otro caso.
"""


def empieza_con_tag_apertura(linea: str) -> bool:
    return linea.startswith(CARACTER_APERTURA_TAG) and not linea.startswith(CARACTER_BARRA_CIERRE_TAG, 1)


"""
// Pre: -

// Post: Devuelve True el slice de línea entre indice_actual e indice_actual + 2 es un CARACTER_CIERRE_TAG.
//       False en cualquier otro caso.
"""


def termina_con_tag_cierre(linea: str, indice_actual: int) -> bool:
    return linea[indice_actual: indice_actual + 2:] == CARACTER_CIERRE_TAG


"""
// Pre: len(linea) > 1.

// Post: Devuelve el tag de apertura aislado de sus caracteres que indican su propósito.
"""


def aislar_tag_apertura(linea: str) -> tuple[str, int]:
    indice_actual = 1
    tag_aislado = ""

    while linea[indice_actual] != ">":
        tag_aislado += linea[indice_actual]
        indice_actual += 1

    return tag_aislado, indice_actual + 1


"""
// Pre: -

// Post: Devuelve el tag de cierre aislado de sus caracateres que indican su propósito.
"""


def aislar_tag_cierre(linea: str, indice_actual: int) -> str:
    return linea[indice_actual + 2: len(linea) - 1:]


"""
// Pre: -

// Post: Devuelve, si existen, el tag de apertura y cierre de linea (en ese orden).
//       De otro modo devuelve NO_EXISTE.
"""


def procesar_linea(linea: str) -> tuple[str]:
    tag_apertura = NO_EXISTE
    tag_cierre = NO_EXISTE
    indice_actual = 0

    if empieza_con_tag_apertura(linea):
        tag_apertura, indice_actual = aislar_tag_apertura(linea)

    try:
        indice_actual = linea.rindex("<")
    except:
        indice_actual += 1

    if termina_con_tag_cierre(linea, indice_actual):
        tag_cierre = aislar_tag_cierre(linea, indice_actual)

    return tag_apertura, tag_cierre


"""
// Pre: len(tags_apertura) >= 1.

// Post: Devuelve, si hay algun error en el formato XML, un mensaje con una breve explicación de este. NO EXISTE si no hay error.
"""


def procesar_posible_error(tags_apertura: list[str], tag_cierre_actual: str) -> str:
    mensaje_error = NO_EXISTE

    if tag_cierre_actual in tags_apertura:
        if tag_cierre_actual != tags_apertura[ULTIMO_TAG_ABIERTO]:
            mensaje_error = f"El archivo cierra el tag '{tag_cierre_actual}' cuando primero tiene que cerrar el tag '{tags_apertura[ULTIMO_TAG_ABIERTO]}'"

        tags_apertura.pop()

    elif tag_cierre_actual != NO_EXISTE:
        mensaje_error = f"El archivo cierra el tag '{tag_cierre_actual}' sin abrirlo previamente."

    return mensaje_error


"""
// Pre: len(tags_apertura) > 0

// Post: Imprime los elementos de tags_apertura uno debajo del otro.
"""


def imprimir_tags_no_cerrados(tags_apertura: str) -> None:

    for tag in tags_apertura:
        print(tag)


"""
// Pre:  -

// Post: Imprime por pantalla mensaje_error si este es distinto de NO_EXISTE.
//       De otra manera imprime los elementos de tags_apertura si este contiene alguno.
//       Finalmente, si no se cumple ninguna de las anteriores, imprime que el formato es válido.
"""


def informar_situacion_validez(tags_apertura: list[str], mensaje_error: str) -> None:
    if mensaje_error != NO_EXISTE:
        print(f"Es un formato inválido, ya que {mensaje_error}")

    elif len(tags_apertura) > 0:
        print("Es un formato inválido, ya que hay tag(s) que nunca se cerraron, listado(s) a continuación:")
        imprimir_tags_no_cerrados(tags_apertura)

    else:
        print("El formato es válido.")


"""
// Post: -

// Post: Se agrega al final de tags_apertura el elemento tags_apertura_actual si este último es distinto de NO_EXISTE.
"""


def agregar_tag_apertura(tags_apertura: list[str], tag_apertura_actual: str) -> None:
    if tag_apertura_actual != NO_EXISTE:
        tags_apertura.append(tag_apertura_actual)


"""
// Pre: path debe ser una dirección existente de un archivo XML.

// Post: Chequea si el archivo provisto es o no un archivo XML válido.
//       De ser una conclusión negativa, explica el porqué de esta decisión. De ser una positiva, lo indica.

"""


def chequear_validez_XML(path: str) -> None:
    tags_apertura = []
    mensaje_error = NO_EXISTE
    tag_apertura_actual = NO_EXISTE
    tag_cierre_actual = NO_EXISTE

    with open(path, "r") as archivo:
        while (linea := archivo.readline().lstrip().rstrip()) and mensaje_error == NO_EXISTE:

            tag_apertura_actual, tag_cierre_actual = procesar_linea(linea)

            agregar_tag_apertura(tags_apertura, tag_apertura_actual)

            mensaje_error = procesar_posible_error(
                tags_apertura, tag_cierre_actual)

    informar_situacion_validez(tags_apertura, mensaje_error)


"""
// Pre: -

// Post: Informa al usuario sobre la validez en el formato XML del archivo provisto por él.
"""


def main() -> None:
    path = input("Ingrese la ruta del archivo XML a validar: ")

    chequear_validez_XML(path)


main()
