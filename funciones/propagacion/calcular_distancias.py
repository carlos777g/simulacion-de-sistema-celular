import numpy as np

def calcular_distancias_reales(usuarios, estaciones_base, altura_bs=19.5):
    """
    Calcula la distancia real 3D entre cada usuario y cada estación base.
    
    Retorna una lista de diccionarios por usuario, con la distancia a cada BS.
    """
    resultados = []

    for ux, uy in usuarios:
        distancias_usuario = []
        for bx, by in estaciones_base:
            dx = ux - bx
            dy = uy - by
            distancia_plana = np.sqrt(dx**2 + dy**2)
            distancia_real = np.sqrt(distancia_plana**2 + altura_bs**2)
            distancias_usuario.append({
                "usuario_xy": (ux, uy),
                "bs_xy": (bx, by),
                "distancia_real": distancia_real,
                "distancia_plana": distancia_plana
            })
        resultados.append(distancias_usuario)

    return resultados
