from funciones.hexagonos.graficar_hexagonos import graficar_malla_hexagonal

if __name__ == "__main__":
    centros_celdas = graficar_malla_hexagonal(radio=1)
    print("Centros de las celdas:", centros_celdas)
