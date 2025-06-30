import numpy as np
import matplotlib.pyplot as plt

from funciones.hexagonos.graficar_hexagonos import graficar_malla_hexagonal, obtener_vertices_hexagono
from funciones.usuarios.generar_usuarios import generar_usuarios_uniformes_en_circulo, graficar_usuarios
from funciones.propagacion.calcular_distancias import calcular_distancias_reales
from funciones.propagacion.modelo_lognormal import model_lognormal

# Parámetros globales
FREQ_MHZ = 1935
Pt_dBm = 10 * np.log10(10) + 30  # 10 W
Gt_dB = 9
Gr_dB = 3
alpha = 2.8
sigma = 7
altura_BS= 19.7
numUsuarios = 10
radio_hex = 400
apotema = radio_hex * (np.sqrt(3)/2)
radio_circulo = np.sqrt((np.power(apotema*3,2))+(np.power(radio_hex/2,2)))

if __name__ == "__main__":
    
    centros_celdas = graficar_malla_hexagonal(radio_hex)
    # Lo siguiente es para calcular el radio del circulo en donde se generaran los usuarios uniformemente
    usuarios = generar_usuarios_uniformes_en_circulo(numUsuarios, radio_circulo)


    # print(usuarios)
    # print("Centros de las celdas:", centros_celdas)

    # Para cada usuario, obtener la pérdida con cada BS
    matriz_potencias = []

    for distancias_usuario in calcular_distancias_reales(usuarios, centros_celdas, altura_bs=15):
        # distancias_usuario = lista de 7 dicts (una por BS)
        potencias = model_lognormal(distancias_usuario, Pt_dBm, Gt_dB, Gr_dB, alpha, sigma)
        matriz_potencias.append(potencias)

    # ...código existente...
    for idx_usuario, potencias_usuario in enumerate(matriz_potencias):
        print(f"\nUsuario {idx_usuario+1}:")
        for idx_bs, datos_bs in enumerate(potencias_usuario):
            print(f"  BS {idx_bs+1}: distancia={datos_bs['distance']:.2f} m, "
                f"pérdida={datos_bs['loss_d']:.2f} dB, "
                f"shadowing={datos_bs['shadowing']:.2f} dB, "
                f"Pr={datos_bs['Pr_log']:.2f} dBm")
    # print("Potencias:", matriz_potencias)
    # Cada entrada de matriz_potencias[i] es una lista con las potencias recibidas
    # del usuario i desde cada BS

    asignaciones = []  # Lista de índices de BS asignado para cada usuario

    for potencias_usuario in matriz_potencias:
        mejor_idx = np.argmax([bs["Pr_log"] for bs in potencias_usuario])
        asignaciones.append(mejor_idx)
    
    print("Asignaciones", asignaciones)

    # Graficamos todo
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    for idx, (cx, cy) in enumerate(centros_celdas):
        x, y = obtener_vertices_hexagono(cx, cy, radio_hex)
        ax.plot(x, y, 'k')
        # ax.fill(x, y, alpha=0.2) Esto para rellenar de color cada celda
        ax.text(cx, cy, f"BS {idx+1}", ha='center', va='center', fontsize=9, color='blue', fontweight='bold')
    
    for i, (x, y) in enumerate(usuarios):
        bs_idx = asignaciones[i]  # Índice de la BS asignada
        ax.text(x, y, str(bs_idx + 1), fontsize=8, color='black', ha='center', va='center')
    
    # graficar_usuarios(ax, usuarios) # Descomentar esto para ver los puntos usuario más claros
    ax.set_title(f"Asociación de usuarios a su mejor estación base ({numUsuarios} usuarios)")
    # ax.legend(title="Usuarios conectados a:")
    ax.grid(True)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show(block=False)
    input("Presiona Enter para cerrar la ventana...")
