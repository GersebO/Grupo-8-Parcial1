"""
agregaciones.py
---------------
Módulo de funciones de agregación y análisis estadístico avanzado con Pandas.
Encapsula las operaciones de groupby y merge para reutilización en notebooks.

Importar en el notebook con:
    import sys; sys.path.append('../src')
    from agregaciones import (
        resumen_costo_por_region,
        top_causas_por_pacientes,
        resumen_demografico_triage,
        calcular_indice_gravedad
    )
"""

import pandas as pd
import numpy as np


def resumen_costo_por_region(df, col_region='RegionGlosa', col_costo='CostoAtencionCLP'):
    """
    Calcula un resumen del costo de atención agrupado por región.
    Utiliza groupby con múltiples funciones de agregación (agg).

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos de urgencias.
        col_region (str): Nombre de la columna de región.
        col_costo (str): Nombre de la columna de costo.

    Retorna:
        pd.DataFrame: Tabla con Costo_Promedio, Costo_Total, Costo_Mediana y N_Registros
                      ordenada de mayor a menor costo total.
    """
    resumen = (
        df.groupby(col_region)[col_costo]
        .agg(
            Costo_Promedio='mean',
            Costo_Mediana='median',
            Costo_Total='sum',
            N_Registros='count'
        )
        .sort_values('Costo_Total', ascending=False)
        .reset_index()
    )
    resumen['Costo_Promedio'] = resumen['Costo_Promedio'].round(0)
    resumen['Costo_Mediana']  = resumen['Costo_Mediana'].round(0)
    return resumen


def top_causas_por_pacientes(df, col_causa='Causa', col_total='NumTotal', n=10):
    """
    Calcula el ranking de causas de urgencia por total de pacientes atendidos,
    usando groupby con agg sobre múltiples columnas.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos de urgencias.
        col_causa (str): Nombre de la columna de causa.
        col_total (str): Nombre de la columna de total de pacientes.
        n (int): Número de causas a retornar (top-N).

    Retorna:
        pd.DataFrame: Top N causas con Total_Pacientes y N_Registros.
    """
    return (
        df.groupby(col_causa)[col_total]
        .agg(Total_Pacientes='sum', N_Registros='count')
        .sort_values('Total_Pacientes', ascending=False)
        .head(n)
        .reset_index()
    )


def resumen_demografico_triage(df,
                                col_triage='TriageEstandarizado',
                                col_sexo='SexoEstandarizado',
                                col_costo='CostoAtencionCLP'):
    """
    Realiza un groupby de doble nivel (triage x sexo) para obtener
    el costo promedio y el total de atenciones por categoría demográfica.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos de urgencias (ya estandarizados).
        col_triage (str): Columna de prioridad triage estandarizada.
        col_sexo (str): Columna de sexo estandarizado.
        col_costo (str): Columna de costo de atención.

    Retorna:
        pd.DataFrame: Tabla pivot con el análisis cruzado triage x sexo.
    """
    resumen = (
        df.groupby([col_triage, col_sexo])[col_costo]
        .agg(Costo_Promedio='mean', N_Atenciones='count')
        .reset_index()
    )
    resumen['Costo_Promedio'] = resumen['Costo_Promedio'].round(0)
    return resumen


def calcular_indice_gravedad(df,
                              col_triage='TriageEstandarizado',
                              col_costo='CostoAtencionCLP',
                              col_total='NumTotal'):
    """
    Calcula un 'Índice de Gravedad' por categoría de triage, definido como
    el costo promedio normalizado multiplicado por el promedio de pacientes.

    Usa NumPy internamente para la normalización vectorizada del índice.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos de urgencias.
        col_triage (str): Columna de triage estandarizado.
        col_costo (str): Columna de costo.
        col_total (str): Columna de total de pacientes.

    Retorna:
        pd.DataFrame: Tabla con el índice de gravedad por categoría de triage,
                      ordenada de mayor a menor.
    """
    base = (
        df.groupby(col_triage)
        .agg(
            Costo_Promedio=(col_costo, 'mean'),
            Pacientes_Promedio=(col_total, 'mean'),
            N_Registros=(col_costo, 'count')
        )
        .reset_index()
    )

    # Vectorización NumPy: normalizar costo promedio entre 0 y 1
    costos = np.array(base['Costo_Promedio'].fillna(0))
    max_costo = np.nanmax(costos)
    costo_norm = costos / max_costo if max_costo > 0 else costos

    # Broadcasting: índice = costo normalizado * pacientes promedio
    pacientes = np.array(base['Pacientes_Promedio'].fillna(0))
    base['Indice_Gravedad'] = np.round(costo_norm * pacientes, 2)

    return base.sort_values('Indice_Gravedad', ascending=False).reset_index(drop=True)


def merge_con_complementario(df_principal, df_complementario,
                              key_left, key_right, how='left'):
    """
    Realiza un merge (join) entre el dataset principal y uno complementario.
    Equivalente a un LEFT/INNER JOIN en SQL.

    Útil para enriquecer el dataset con información externa
    (ej: tabla de establecimientos, metadata regional, etc.)

    Parámetros:
        df_principal (pd.DataFrame): DataFrame base (el dataset de urgencias).
        df_complementario (pd.DataFrame): DataFrame con datos a unir.
        key_left (str): Columna clave en el df_principal.
        key_right (str): Columna clave en el df_complementario.
        how (str): Tipo de join: 'left', 'inner', 'right', 'outer'.

    Retorna:
        pd.DataFrame: DataFrame resultante del merge.
    """
    resultado = pd.merge(
        df_principal,
        df_complementario,
        left_on=key_left,
        right_on=key_right,
        how=how
    )
    print(f"[merge] Filas antes: {len(df_principal)} → después: {len(resultado)} (how='{how}')")
    return resultado
