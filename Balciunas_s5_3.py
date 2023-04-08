import pickle

MAX_ID = 999999
NUMERO_ID = 0
CANTIDAD_STOCK = 1
CANTIDAD_CAMPOS = 2

"""
// Pre: archivo debe estar abierto correctamente.

// Post: Devuelve el tamaño del archivo.

"""


def devolver_tamaño_archivo(archivo) -> int:
    archivo.seek(0, 2)
    tamaño_archivo = archivo.tell()
    archivo.seek(0)

    return tamaño_archivo


"""
// Pre: archivo_novedad y archivo_errores deben estar abiertos en las siguientes condiciones:

//      Para el primero, en modo de lectura. Para el segundo en modo de escritura.

// Post: Devuelve la primera línea no leída de formato valido de archivo_novedad.
//       De no existir devuelve un único elemento; MAX_ID
"""


def leer_novedad(archivo_novedad, archivo_errores) -> list[int]:
    lista_informacion_novedad = [MAX_ID]
    linea_valida = False

    while not linea_valida and (linea := archivo_novedad.readline()):
        novedad = linea.rstrip().split(",")

        if not len(novedad) == CANTIDAD_CAMPOS:
            archivo_errores.write(linea)
        else:
            try:
                novedad[NUMERO_ID] = int(novedad[NUMERO_ID])
                novedad[CANTIDAD_STOCK] = int(novedad[CANTIDAD_STOCK])
                lista_informacion_novedad = novedad
                linea_valida = True

            except ValueError:
                archivo_errores.write(linea)

    return lista_informacion_novedad


"""
// Pre: archivo_stock y archivo_errores deben estar abiertos en las siguientes condiciones:

//      Para el primero, en modo de lectura binaria. Para el segundo en modo de escritura.

// Post: Devuelve la primera línea no leída de formato válido de archivo_stock.
//       De no existir devuelve un único elemento; MAX_ID
"""


def leer_stock(archivo_stock, archivo_errores, tamaño_archivo: int) -> list[int]:
    registro_stock = [MAX_ID]
    linea_valida = False

    while not linea_valida and archivo_stock.tell() < tamaño_archivo:
        registro_stock = pickle.load(archivo_stock)

        if not len(registro_stock) == CANTIDAD_CAMPOS:
            archivo_errores.write(procesar_linea(registro_stock))
        else:
            try:
                registro_stock[NUMERO_ID] = int(registro_stock[NUMERO_ID])
                registro_stock[CANTIDAD_STOCK] = int(
                    registro_stock[CANTIDAD_STOCK])
                linea_valida = True

            except ValueError:
                archivo_errores.write(procesar_linea(registro_stock))

    return registro_stock


"""
// Pre: len(registro_stocks) > CANTIDAD_STOCK, len(novedad) > CANTIDAD_STOCK.
//      archivo_stock_actualizado debe estar correctamente abierto en modo de escritura binaria.

// Post: Añade a archivo_stock_actualizado una lista que contiene:

//       Indice 0: el valor del índice 0 de novedad
//       Indice 1: la resta entre el valor de índice 1 de registro_stock y el de novedad, en ese orden.
"""


def procesar_actualizacion(registro_stock: list[int], novedad: list[int], archivo_stock_actualizado) -> None:
    valor_actualizado = [novedad[NUMERO_ID],
                         registro_stock[CANTIDAD_STOCK]
                         - novedad[CANTIDAD_STOCK]]

    pickle.dump(valor_actualizado, archivo_stock_actualizado)


"""
// Pre: len(novedad) > CANTIDAD_STOCK

// Post: Devuelve los primeros dos elementos de novedad, separados por una coma.
"""


def procesar_linea(novedad: list[int]) -> str:
    return "{},{}\n".format(novedad[NUMERO_ID], novedad[CANTIDAD_STOCK])


"""
// Pre: len(novedad) > CANTIDAD_STOCK, len(registro_stock) > CANTIDAD_STOCK.

// Post: Devuelve True si no se invalida la resta entre los valores de índice 1 de registro_stock y novedad
//       y también los valores de índice 0 de las anteriores nombradas son iguales y menores que MAX_ID
"""


def hay_concidencia(novedad: list[int], registro_stock: list[int]) -> bool:
    no_se_invalida_resta = registro_stock[CANTIDAD_STOCK] > novedad[CANTIDAD_STOCK]

    coincidencia_entre_ID = novedad[NUMERO_ID] == registro_stock[NUMERO_ID] and novedad[
        NUMERO_ID] != MAX_ID and registro_stock[NUMERO_ID] != MAX_ID

    return coincidencia_entre_ID and no_se_invalida_resta


"""
// Pre: Todos los archivos deben estar correctamente abiertos en las siguientes condiciones:
//      Para el primero, en lectura binaria. Para el segundo, en lectura. Para el tercero, en escritura binaria.
//      Por último, para el cuarto; en escritura.

//      archivo_stock y archivo_novedades deben tener el mismo formato.

// Post: Realiza un apareo entre archivo_stock y archivo_novedades, y lo deposita en archivo_stock_actualizado.
//       De haber algún error lo deposita en archivo_errores.
"""


def actualizar_stock(archivo_stock, archivo_novedades, archivo_stock_actualizado, archivo_errores) -> None:
    tamaño_archivo = devolver_tamaño_archivo(archivo_stock)
    novedad = leer_novedad(archivo_novedades, archivo_errores)
    registro_stock = leer_stock(archivo_stock, archivo_errores, tamaño_archivo)

    while novedad[NUMERO_ID] < MAX_ID or registro_stock[NUMERO_ID] < MAX_ID:
        minimo = min(novedad[NUMERO_ID], registro_stock[NUMERO_ID])

        while len(novedad) > 1 and len(registro_stock) > 1 and hay_concidencia(novedad, registro_stock):
            procesar_actualizacion(registro_stock, novedad,
                                   archivo_stock_actualizado)

            novedad = leer_novedad(archivo_novedades, archivo_errores)
            registro_stock = leer_stock(archivo_stock, archivo_errores, tamaño_archivo)

        while novedad[NUMERO_ID] == minimo:
            archivo_errores.write(procesar_linea(novedad))
            novedad = leer_novedad(archivo_novedades, archivo_errores)

        while registro_stock[NUMERO_ID] == minimo:
            pickle.dump(registro_stock, archivo_stock_actualizado)
            registro_stock = leer_stock(archivo_stock, archivo_errores, tamaño_archivo)


"""
// Pre: -

// Post: Realiza un apareo entre archivo_stock y archivo_novedades, y lo deposita en archivo_stock_actualizado.
"""


def main() -> None:
    archivo_stock = open("stock.dat", "rb")
    archivo_novedades = open("novedades.csv", "r")
    archivo_stock_actualizado = open("stock_actualizado.dat", "wb")
    archivo_errores = open("archivo_errores.txt", "w")

    """with open("stock.dat", "rb") as archivo_stock, open("novedades.csv", "r") as archivo_novedades, open("stock_actualizado.dat", "wb") as archivo_stock_actualizado, open("archivo_errores1.txt", "w") as archivo_errores:"""
    actualizar_stock(archivo_stock, archivo_novedades,
                     archivo_stock_actualizado, archivo_errores)

    archivo_stock.close()
    archivo_novedades.close()
    archivo_stock_actualizado.close()
    archivo_errores.close()


main()
