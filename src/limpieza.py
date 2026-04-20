"""
limpieza.py
-----------
Módulo de funciones de limpieza y estandarización de datos.
Importar en el notebook con:
    import sys; sys.path.append('../src')
    from limpieza import normalizar_fecha, estandarizar_sexo, estandarizar_triage
"""

import re
from datetime import datetime


def normalizar_fecha(fecha_str):
    """
    Normaliza una cadena de texto con formato de fecha variable
    al formato estándar YYYY-MM-DD.

    Formatos soportados:
        - DD-MM-YYYY  (ej: 02-01-2023)
        - DD.MM.YYYY  (ej: 02.01.2023)
        - DD/MM/YYYY  (ej: 02/01/2023)
        - DD.MM.YY    (ej: 02.01.23)
        - DD-MM-YY    (ej: 02-01-23)

    Parámetros:
        fecha_str (str): Cadena de texto con la fecha.

    Retorna:
        str: Fecha en formato YYYY-MM-DD, o None si no se puede parsear.
    """
    if not isinstance(fecha_str, str) or not fecha_str.strip():
        return None

    # Normalizar separadores: reemplazar '.' y '/' por '-'
    fecha_normalizada = re.sub(r'[./]', '-', fecha_str.strip())

    formatos = ['%d-%m-%Y', '%d-%m-%y']
    for fmt in formatos:
        try:
            return datetime.strptime(fecha_normalizada, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue

    return None  # No se pudo parsear


def estandarizar_sexo(valor):
    """
    Estandariza los valores de la columna SexoPaciente a las categorías:
        - 'M'  (Masculino)
        - 'F'  (Femenino)
        - 'I'  (Indeterminado / No informado)

    Parámetros:
        valor (str): Valor original de la columna.

    Retorna:
        str: Categoría estandarizada.
    """
    if not isinstance(valor, str):
        return 'I'

    valor = valor.strip().upper()

    masculino = {'M', 'MASCULINO', 'MALE', 'H', 'HOMBRE'}
    femenino = {'F', 'FEMENINO', 'FEMALE', 'MUJER'}

    if valor in masculino:
        return 'M'
    elif valor in femenino:
        return 'F'
    else:
        return 'I'


def estandarizar_triage(valor):
    """
    Estandariza los valores de la columna PrioridadTriage a las categorías
    válidas del sistema de triage: C1, C2, C3, C4, C5.

    Parámetros:
        valor (str): Valor original de la columna.

    Retorna:
        str: Categoría de triage estandarizada, o 'DESCONOCIDO' si es inválida.
    """
    categorias_validas = {'C1', 'C2', 'C3', 'C4', 'C5'}

    if not isinstance(valor, str):
        return 'DESCONOCIDO'

    valor = valor.strip().upper()

    if valor in categorias_validas:
        return valor

    return 'DESCONOCIDO'
