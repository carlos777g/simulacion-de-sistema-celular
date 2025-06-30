from funciones.utils.tabla_cqi import cqi_table

def asociar_cqi_y_tasa(sirs_db, ancho_banda_mhz=10):
    """
    Asocia la SIR de cada usuario a un CQI, eficiencia espectral y tasa de bits.

    Params:
    - sirs_db: lista de SIRs por usuario en dB
    - ancho_banda_mhz: ancho de banda total en MHz (por defecto 10 MHz)

    Returns:
    - Lista de diccionarios: CQI, eficiencia, tasa_bps
    """
    resultados = []

    for sir in sirs_db:
        cqi_asignado = 0
        bits = 0
        code_rate = 0

        for entrada in reversed(cqi_table):
            if sir >= entrada["SIR_dB"]:
                cqi_asignado = entrada["CQI"]
                bits = entrada["bits"]
                code_rate = entrada["code_rate"]
                break

        eficiencia = bits * code_rate  # bits/Hz
        tasa_bps = eficiencia * ancho_banda_mhz * 1e6  # convertimos MHz a Hz

        resultados.append({
            "SIR_dB": sir,
            "CQI": cqi_asignado,
            "eficiencia": eficiencia,
            "tasa_bps": tasa_bps
        })

    return resultados
