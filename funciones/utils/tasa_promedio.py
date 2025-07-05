# funciones/calculo/tasa_promedio.py

def calcular_tasa_promedio_cqi(resultados_cqi, ancho_banda_hz):
    """
    Calcula la tasa promedio del sistema en bits/s según los resultados CQI.

    Parámetros:
    - resultados_cqi: lista de dicts, cada uno con clave 'CQI' y 'eficiencia' (bits/Hz).
      Esta es la salida de asociar_cqi_y_tasa().
    - ancho_banda_hz: ancho de banda total en Hz (p.ej. 4500 o 1500).

    Retorna:
    - tasa_promedio_bps: float con la tasa promedio en bits/s.
    """
    N = len(resultados_cqi)
    if N == 0:
        return 0.0

    # sumamos E_i para cada usuario
    suma_ef = sum(res["eficiencia"] for res in resultados_cqi)
    # promedio de eficiencia espectral
    ef_promedio = suma_ef / N

    # R = BW * ef_promedio
    return ancho_banda_hz * ef_promedio
