"""
transformaciones.py
-------------------
Módulo de transformaciones avanzadas utilizando NumPy (vectorización y broadcasting).
Importar en el notebook con:
    import sys; sys.path.append('../src')
    from transformaciones import convertir_a_usd, calcular_costo_con_iva, calcular_estadisticas
"""

import numpy as np


def convertir_a_usd(array_clp, tasa_cambio=950.0):
    """
    Convierte un arreglo de costos en pesos chilenos (CLP) a dólares (USD)
    utilizando broadcasting de NumPy. Opera sobre todo el arreglo sin loops.

    Parámetros:
        array_clp (np.ndarray): Arreglo con costos en CLP.
        tasa_cambio (float): Tasa de cambio CLP por 1 USD (por defecto 950).

    Retorna:
        np.ndarray: Arreglo con costos en USD, redondeado a 2 decimales.
    """
    array_clp = np.array(array_clp, dtype=float)
    # Broadcasting: divide cada elemento del array por la tasa (escalar)
    return np.round(array_clp / tasa_cambio, 2)


def calcular_costo_con_iva(array_clp, tasa_iva=0.19):
    """
    Aplica IVA a un arreglo de costos en CLP usando vectorización de NumPy.
    Equivale a multiplicar cada elemento por (1 + tasa_iva) sin ningún loop.

    Parámetros:
        array_clp (np.ndarray): Arreglo con costos base en CLP.
        tasa_iva (float): Tasa de IVA a aplicar (por defecto 19%).

    Retorna:
        np.ndarray: Arreglo con costos incluyendo IVA, redondeado a 0 decimales.
    """
    array_clp = np.array(array_clp, dtype=float)
    # Vectorización: multiplica todo el array por el escalar (1 + tasa_iva)
    return np.round(array_clp * (1 + tasa_iva), 0)


def calcular_estadisticas(array):
    """
    Calcula estadísticas descriptivas clave de un arreglo numérico
    utilizando las funciones vectorizadas de NumPy.

    Parámetros:
        array (np.ndarray): Arreglo numérico de entrada.

    Retorna:
        dict: Diccionario con media, mediana, desviación estándar, mínimo y máximo.
    """
    array_limpio = np.array(array, dtype=float)
    # Ignorar NaN en los cálculos para robustez
    return {
        'media':    np.nanmean(array_limpio),
        'mediana':  np.nanmedian(array_limpio),
        'std':      np.nanstd(array_limpio),
        'min':      np.nanmin(array_limpio),
        'max':      np.nanmax(array_limpio),
    }


def detectar_outliers_iqr(array):
    """
    Detecta outliers en un arreglo utilizando el método IQR (Rango Intercuartílico).
    Un valor es outlier si está por debajo de Q1 - 1.5*IQR o sobre Q3 + 1.5*IQR.

    Parámetros:
        array (np.ndarray): Arreglo numérico de entrada.

    Retorna:
        dict: Contiene los límites inferior/superior, la máscara de outliers y su conteo.
    """
    array_limpio = np.array(array, dtype=float)
    q1 = np.nanpercentile(array_limpio, 25)
    q3 = np.nanpercentile(array_limpio, 75)
    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    # Broadcasting: compara todo el arreglo contra los límites escalares
    mascara_outliers = (array_limpio < limite_inferior) | (array_limpio > limite_superior)

    return {
        'limite_inferior': limite_inferior,
        'limite_superior': limite_superior,
        'mascara_outliers': mascara_outliers,
        'n_outliers': int(np.sum(mascara_outliers)),
    }
