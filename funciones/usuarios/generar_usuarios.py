import numpy as np

def generar_usuarios_uniformes_en_circulo(num_usuarios, radio_circulo, centro=(0, 0)):
    """
    Genera coordenadas de usuarios distribuidos uniformemente en un círculo.
    
    Parámetros:
    - num_usuarios: número de usuarios a generar.
    - radio_circulo: radio del círculo donde se distribuirán.
    - centro: tupla (x, y) del centro del círculo.
    
    Retorna:
    - Lista de tuplas (x, y) con coordenadas de usuarios.
    """
    cx, cy = centro
    radios = np.sqrt(np.random.uniform(0, 1, num_usuarios)) * radio_circulo
    angulos = np.random.uniform(0, 2 * np.pi, num_usuarios)

    x = cx + radios * np.cos(angulos)
    y = cy + radios * np.sin(angulos)

    return list(zip(x, y))

def graficar_usuarios(ax, usuarios, color='red', etiqueta='Usuarios'):
    """
    Grafica usuarios en un Axes existente (usualmente el mismo de la malla).
    """
    if not usuarios:
        return

    x, y = zip(*usuarios)
    ax.scatter(x, y, c=color, s=10, label=etiqueta)
