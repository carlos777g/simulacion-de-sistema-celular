import matplotlib.pyplot as plt
import numpy as np

def obtener_vertices_hexagono(coorX, coorY, radio):
    """
    Calcula los vértices de un hexágono con orientación horizontal (flat-top),
    centrado en (coorX, coorY).
    """
    angulos = np.linspace(0, 2 * np.pi, 7) + np.pi / 6  # Rotamos 30° para orientación horizontal
    x = coorX + radio * np.cos(angulos)
    y = coorY + radio * np.sin(angulos)
    return x, y

def coordenadas_vecinos(coorX, coorY, radio):
    """
    Devuelve los centros de los 6 hexágonos vecinos a uno central (flat-top).
    """
    R = radio
    desplazamientos = [
        (np.sqrt(3) * R, 0),           # E
        (np.sqrt(3)/2 * R, 1.5 * R),   # NE
        (-np.sqrt(3)/2 * R, 1.5 * R),  # NW
        (-np.sqrt(3) * R, 0),          # W
        (-np.sqrt(3)/2 * R, -1.5 * R), # SW
        (np.sqrt(3)/2 * R, -1.5 * R),  # SE
    ]
    vecinos = [(coorX + dx, coorY + dy) for dx, dy in desplazamientos]
    return vecinos


def graficar_malla_hexagonal(radio=1):
    """
    Devuelve los centros de los hexágonos.
    """
    centros = [(0, 0)] + coordenadas_vecinos(0, 0, radio)
    return centros  # Coordenadas centrales de los 7 hexágonos
