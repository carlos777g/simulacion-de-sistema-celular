import matplotlib.pyplot as plt
from collections import Counter

def graficar_histograma_cqi(resultados_cqi):
    """
    Genera un histograma con la distribución de CQI de los usuarios.
    """
    # Contamos cuántos usuarios tienen cada CQI
    cqi_counts = Counter(res["CQI"] for res in resultados_cqi if res["CQI"] is not None)

    # Asegurar que se grafican todos los CQI (1 a 15)
    cqi_vals = list(range(1, 16))
    counts = [cqi_counts.get(cqi, 0) for cqi in cqi_vals]

    # Gráfico
    plt.figure(figsize=(10, 5))
    bars = plt.bar(cqi_vals, counts, color="skyblue", edgecolor="black")
    
    # Añadir etiquetas en las barras
    for bar in bars:
        yval = bar.get_height()
        if yval > 0:
            plt.text(bar.get_x() + bar.get_width()/2, yval + 1, str(yval),
                     ha='center', va='bottom', fontsize=8)

    plt.xticks(cqi_vals)
    plt.xlabel("CQI")
    plt.ylabel("Número de usuarios")
    plt.title("Distribución de CQI asignado a los usuarios")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
