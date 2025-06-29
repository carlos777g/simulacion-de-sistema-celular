import numpy as np
import matplotlib.pyplot as plt

from funciones.hexagonos.graficar_hexagonos import graficar_malla_hexagonal, obtener_vertices_hexagono
from funciones.usuarios.generar_usuarios import generar_usuarios_uniformes_en_circulo, graficar_usuarios

if __name__ == "__main__":
    radio_hex = 1
    centros_celdas = graficar_malla_hexagonal(radio_hex)
    # Lo siguiente es para calcular el radio del circulo en donde se generaran los usuarios uniformemente
    apotema = radio_hex * (np.sqrt(3)/2)
    radio_circulo = np.sqrt((np.power(apotema*3,2))+(np.power(radio_hex/2,2)))
    usuarios = generar_usuarios_uniformes_en_circulo(50, radio_circulo)

    # Graficamos todo
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    for cx, cy in centros_celdas:
        x, y = obtener_vertices_hexagono(cx, cy, radio_hex)
        ax.plot(x, y, 'k')
        ax.fill(x, y, alpha=0.2)

    graficar_usuarios(ax, usuarios)

    ax.set_title("Usuarios distribuidos uniformemente alrededor de la malla hexagonal")
    ax.legend()
    ax.grid(True)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show(block=False)
    print(usuarios)
    print("Centros de las celdas:", centros_celdas)
    input("Presiona Enter para cerrar la ventana...")
