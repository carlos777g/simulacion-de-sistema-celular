import numpy as np

def calcular_sir_por_usuario(matriz_potencias, asignaciones):
    """
    Calcula la SIR para cada usuario.

    Parameters:
    - matriz_potencias: lista de listas, donde cada sublista contiene 7 diccionarios con 'Pr_log' (potencia en dBm)
    - asignaciones: lista con el índice de la BS asignada para cada usuario

    Returns:
    - Lista de SIRs en dB para cada usuario
    """
    sirs_db = []

    for i, potencias_usuario in enumerate(matriz_potencias):
        bs_asignada = asignaciones[i]

        # Potencia útil en dBm → mW
        p_util_dbm = potencias_usuario[bs_asignada]["Pr_log"]
        p_util_mw = 10 ** (p_util_dbm / 10)

        # Potencias interferentes
        p_interferentes_mw = [
            10 ** (p["Pr_log"] / 10)
            for j, p in enumerate(potencias_usuario) if j != bs_asignada
        ]

        suma_interferencia = np.sum(p_interferentes_mw)

        sir = p_util_mw / suma_interferencia if suma_interferencia > 0 else np.inf
        sir_db = 10 * np.log10(sir)
        sirs_db.append(sir_db)

    return sirs_db
