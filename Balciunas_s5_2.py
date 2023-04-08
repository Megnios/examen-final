NUMERO_DIA = 0
NOMBRE_EQUIPO_1 = 1
GOLES_EQUIPO_1 = 2
NOMBRE_EQUIPO_2 = 3
GOLES_EQUIPO_2 = 4
CANTIDAD_CAMPOS = 5
AÑO_MUNDIAL_2018 = 2018
AÑO_MUNDIAL_2022 = 2022
MAX_DIA = 99999

"""
// Pre: len(informacion) > 4.

// Post: Devuelve parametro_a_añadir seguido de los 5 primeros elementos de informacion, todos separados con comas.
"""


def procesar_informacion(informacion: list, parametro_a_añadir: int) -> str:
    return "{},{},{},{},{},{}\n".format(parametro_a_añadir, informacion[NUMERO_DIA], informacion[NOMBRE_EQUIPO_1],
                                        informacion[GOLES_EQUIPO_1], informacion[NOMBRE_EQUIPO_2],
                                        informacion[GOLES_EQUIPO_2])


"""
// Pre: archivo1 y archivo2 deben tener el mismo formato.
//      Todos los archivos deben existir y estar abiertos en las siguientes condiciones:
//
//      Para los primeros dos, en lectura. Para los últimos dos en escritura.

// Post: Realiza un merge entre archivo1 y archivo dos y lo deposita en archivo_merge.
//       Las líneas inválidas se depositan en archivo_errores.
"""


def merge(archivo1, archivo2, archivo_merge, archivo_errores) -> None:
    informacion2018 = leer_linea(archivo1, archivo_errores)
    informacion2022 = leer_linea(archivo2, archivo_errores)

    while informacion2018[NUMERO_DIA] < MAX_DIA or informacion2022[NUMERO_DIA] < MAX_DIA:
        minimo = min(informacion2018[NUMERO_DIA],
                     informacion2022[NUMERO_DIA])

        while informacion2018[NUMERO_DIA] == minimo:
            archivo_merge.write(procesar_informacion(informacion2018, AÑO_MUNDIAL_2018))
            informacion2018 = leer_linea(archivo1, archivo_errores)

        while informacion2022[NUMERO_DIA] == minimo:
            archivo_merge.write(procesar_informacion(informacion2022, AÑO_MUNDIAL_2022))
            informacion2022 = leer_linea(archivo2, archivo_errores)


"""
// Pre: archivo_lectura y archivo_errores deben ser archivos existentes.
//      El primero debe haberse abierto en modo lectura, el segundo en modo de escritura.
//      archivo_lectura debe estar en formato csv.

// Post: Devuelve la primera linea que no se haya leido de archivo_lectura cuyo formato sea válido.
//       Si el formato de la línea leída no es válido, se la deposita en archivo_errores.
"""


def leer_linea(archivo_lectura, archivo_errores) -> list:
    lista_informacion = [MAX_DIA]
    linea_valida = False

    while not linea_valida and (linea := archivo_lectura.readline()):
        informacion = linea.rstrip().split(",")

        if not len(informacion) == CANTIDAD_CAMPOS:
            archivo_errores.write(linea)
        else:
            try:
                informacion[GOLES_EQUIPO_1] = int(informacion[GOLES_EQUIPO_1])
                informacion[GOLES_EQUIPO_2] = int(informacion[GOLES_EQUIPO_2])
                informacion[NUMERO_DIA] = int(informacion[NUMERO_DIA])
                lista_informacion = informacion
                linea_valida = True

            except ValueError:
                archivo_errores.write(linea)

    return lista_informacion


"""
// Pre: Los values de cada key deben poder admitir comparación entre si.

// Post: Devuelve diccionario_paises ordenado descendentemente por los values de sus key.
"""


def ordenar_paises_por_partidos(diccionario_paises: dict) -> dict:
    return dict(sorted(diccionario_paises.items(), key=lambda x: x[1], reverse=True))


"""
// Pre: len(informacion_paises) > 5. diccionario_paises debe tener dos key:
//      una que coincida con informacion_paises[NOMBRE_EQUIPO_1]
        y otra que coincida con informacion_paises[NOMBRE_EQUIPO_2].
        Los values de las antes mencionadas deben ser de tipo int o float y poder admitir comparación entre sí.

// Post: Se le suma 1 al value de la key que coincida en nombre con el equipo que convirtió más goles. 
"""


def modificar_informacion_pais(informacion_paises: list, diccionario_paises: dict) -> None:

    if informacion_paises[GOLES_EQUIPO_1] > informacion_paises[GOLES_EQUIPO_2]:
        diccionario_paises[informacion_paises[NOMBRE_EQUIPO_1]] += 1

    elif informacion_paises[GOLES_EQUIPO_2] > informacion_paises[GOLES_EQUIPO_1]:
        diccionario_paises[informacion_paises[NOMBRE_EQUIPO_2]] += 1


"""
// Pre: len(informacion_paises) > 4

// Post: Chequea si existe una key que coincida en valor con informacion_paises[NOMBRE_EQUIPO_1] o informacion_paises[NOMBRE_EQUIPO_2].
//       Si existe le asigna un 0 como value.
"""


def chequear_existencia_pais(informacion_paises: list, diccionario_paises: dict) -> None:
    if informacion_paises[NOMBRE_EQUIPO_1] not in diccionario_paises:
        diccionario_paises[informacion_paises[NOMBRE_EQUIPO_1]] = 0

    if informacion_paises[NOMBRE_EQUIPO_2] not in diccionario_paises:
        diccionario_paises[informacion_paises[NOMBRE_EQUIPO_2]] = 0


"""
// Pre: archivomerge debe estar abierto en el modo de lectura. También debe ser formato csv.

// Post: Devuelve un diccionario con key 'nombre del país' y value 'cantidad de partidos ganados'
"""


def crear_diccionario_mundial(archivomerge) -> dict:
    diccionario_paises = {}

    while (linea := archivomerge.readline()):
        informacion_paises = linea.rstrip().split(",")
        informacion_paises.pop(0)

        chequear_existencia_pais(informacion_paises, diccionario_paises)
        modificar_informacion_pais(informacion_paises, diccionario_paises)

    return diccionario_paises


"""
// Pre: diccionario_paises debe tener una key por lo menos.

// Post: Imprime una tabla con formato key, value separado por barras.
"""


def imprimir_paises(diccionario_paises: dict) -> None:

    print("{:^20} {:<4} {:>10}".format(
        "Nombre del país", "|", "Partidos ganados"))
    print("{:>22}".format("|"))

    for key, value in diccionario_paises.items():
        print("{:^20} | {:^20}".format(key, value))
    print("----------------------------------------------------\n")


"""
// Pre: diccionario_paises debe tener una key por lo menos.

// Post: Imprime una tabla con formato key, value separado por barras.
//       Excluye las key cuyo value sea 0.
"""


def imprimir_paises_ganadores(diccionario_paises: dict) -> None:

    print("{:^20} {:<4} {:>10}".format(
        "Nombre del país", "|", "Partidos ganados"))
    print("{:>22}".format("|"))

    for key, value in diccionario_paises.items():
        if value != 0:
            print("{:^20} | {:^20}".format(key, value))


"""
// Pre: -

// Post: Crea 'archivo_merge.txt' y 'archivo_errores.txt' a partir de 'resultados_2018.txt' y 'resultados_2022.txt'.
//       A partir de los datos del primer archivo crea un diccionario con key: 'nombre del país' y value: 'cantidad de partidos ganados'.
//       Crea otro diccionario ordenado por cantidad de partidos ganados a partir del primero. Imprime ambos en formato tabla, en ese orden.
"""


def main() -> None:

    archivo1 = open("resultados_2018.txt", "r")
    archivo2 = open("resultados_2022.txt", "r")
    archivo_merge = open("archivo_merge.txt", "w")
    archivo_errores = open("archivo_errores.txt", "w")

    merge(archivo1, archivo2, archivo_merge, archivo_errores)

    archivo1.close()
    archivo2.close()
    archivo_merge.close()
    archivo_errores.close()

    with open("archivo_merge.txt", "r") as archivo_merge:

        print("DICCIONARIO CON TODOS LOS PAISES\n")
        diccionario_paises = crear_diccionario_mundial(archivo_merge)
        imprimir_paises(diccionario_paises)

        print("DICCIONARIO SOLO CON LOS PAISES GANADORES\n")
        diccionario_ordenado = ordenar_paises_por_partidos(diccionario_paises)
        imprimir_paises_ganadores(diccionario_ordenado)


main()
