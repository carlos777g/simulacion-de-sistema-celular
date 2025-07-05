def calcular_tasa_promedio_cqi(resultados_cqi, ancho_banda_hz):
    """
    Calcula la tasa promedio del sistema en Mbps con base en la eficiencia espectral promedio
    y el ancho de banda total.

    Parámetros:
    - resultados_cqi: lista de dicts, cada uno con la clave "eficiencia"
    - ancho_banda_hz: ancho de banda en Hz

    Retorna:
    - Tasa promedio en Mbps (float)
    """
    N = len(resultados_cqi)
    if N == 0:
        return 0.0  # evitar división por cero

    eficiencia_total = sum(res["eficiencia"] for res in resultados_cqi)
    eficiencia_promedio = eficiencia_total / N

    R_bps = ancho_banda_hz * eficiencia_promedio
    R_mbps = R_bps / 1e6

    return R_mbps
