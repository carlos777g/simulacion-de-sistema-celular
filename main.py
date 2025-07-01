import numpy as np
import matplotlib.pyplot as plt
import json

from funciones.hexagonos.graficar_hexagonos import graficar_malla_hexagonal, obtener_vertices_hexagono
from funciones.usuarios.generar_usuarios import generar_usuarios_uniformes_en_circulo, graficar_usuarios
from funciones.propagacion.calcular_distancias import calcular_distancias_reales
from funciones.propagacion.modelo_lognormal import model_lognormal
from funciones.propagacion.calcular_sir import calcular_sir_por_usuario
from funciones.propagacion.asociar_cqi import asociar_cqi_y_tasa

# Parámetros globales
FREQ_MHZ = 1935
Pt_dBm = 10 * np.log10(10) + 30  # 10 W
Gt_dB = 9
Gr_dB = 3
alpha = 2.8
sigma = 7
altura_BS= 19.7
numUsuarios = 400
radio_hex = 400
apotema = radio_hex * (np.sqrt(3)/2)
radio_circulo = np.sqrt((np.power(apotema*3,2))+(np.power(radio_hex/2,2)))
ancho_banda_mhz = 0.18

if __name__ == "__main__":
    
    centros_celdas = graficar_malla_hexagonal(radio_hex)
    # Lo siguiente es para calcular el radio del circulo en donde se generaran los usuarios uniformemente
    usuarios = generar_usuarios_uniformes_en_circulo(numUsuarios, radio_circulo)


    # print(usuarios)
    # print("Centros de las celdas:", centros_celdas)

    # Para cada usuario, obtener la pérdida con cada BS
    matriz_potencias = []

    for distancias_usuario in calcular_distancias_reales(usuarios, centros_celdas, altura_BS):
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
        mejor_idx = np.argmin([bs["loss_d"] for bs in potencias_usuario])
        asignaciones.append(mejor_idx)
    
    print("Asignaciones", asignaciones)

    # Calcular la SIR de cada usuario:
    sirs = calcular_sir_por_usuario(matriz_potencias, asignaciones)

    # Imprimir SIR
    for i, sir_db in enumerate(sirs):
        print(f"Usuario {i+1}: SIR = {sir_db:.2f} dB")
    
    # Asociar cqi
    resultados_cqi = asociar_cqi_y_tasa(sirs, ancho_banda_mhz)

    for i, res in enumerate(resultados_cqi):
        print(f"Usuario {i+1}: SIR = {res['SIR_dB']:.2f} dB, "
            f"CQI = {res['CQI']}, "
            f"Eficiencia espectral= {res['eficiencia']:.3f} "
              f"Tasa = {res['tasa_bps'] / 1e6:.2f} Mbps")
    
    # Guardar en JSON
    # Extraer solo los usuarios asociados a BS1 (índice 0)
    usuarios_bs1 = []
    for i, bs in enumerate(asignaciones):
        if bs == 0:  # BS1 tiene índice 0
            datos = {
                "usuario_id": i + 1,
                "x": usuarios[i][0],
                "y": usuarios[i][1],
                "loss_d": matriz_potencias[i][0]["loss_d"],
                "shadowing": matriz_potencias[i][0]["shadowing"],
                "Pr_log": matriz_potencias[i][0]["Pr_log"],
                "SIR_dB": sirs[i]
            }
            usuarios_bs1.append(datos)

    # Guardar en JSON
    with open("usuarios_bs1_k1.json", "w") as f:
        json.dump(usuarios_bs1, f, indent=4)

    print(f"\nSe guardaron {len(usuarios_bs1)} usuarios asociados a BS1 en 'usuarios_bs1_k1.json'")


    # Graficando celdas y usuarios
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