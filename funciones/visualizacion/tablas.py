from rich.console import Console
from rich.table import Table

def tabla_resumen_usuarios(usuarios, matriz_potencias, asignaciones, num_bs=7, limite=10):
    """
    Genera y retorna una tabla Rich con la información de los primeros usuarios.

    Parámetros:
    - usuarios: lista de coordenadas (x, y)
    - matriz_potencias: lista de listas con datos de pérdidas hacia cada BS
    - asignaciones: lista con índice de BS asignada para cada usuario
    - num_bs: número de estaciones base (por defecto 7)
    - limite: número de usuarios a mostrar (por defecto 10)
    """
    console = Console()
    table = Table(title=f"[bold cyan]Resumen de los {limite} primeros usuarios")

    table.add_column("Usuario", justify="center", style="bold")
    table.add_column("X", justify="right")
    table.add_column("Y", justify="right")
    
    for i in range(num_bs):
        table.add_column(f"Loss BS{i+1}", justify="right")
    
    table.add_column("BS asignada", justify="center", style="green")

    for i in range(min(limite, len(usuarios))):
        fila = [
            str(i + 1),
            f"{usuarios[i][0]:.2f}",
            f"{usuarios[i][1]:.2f}",
            *[f"{matriz_potencias[i][j]['loss_d']:.2f}" for j in range(num_bs)],
            str(asignaciones[i] + 1)
        ]
        table.add_row(*fila)

    console.print(table)


# Para punto 3
def mostrar_coordenadas_bs(centros_celdas):
    table = Table(title="[bold cyan]Coordenadas de las Estaciones Base (BS)[/bold cyan]")
    table.add_column("BS", justify="center", style="bold")
    table.add_column("X", justify="right")
    table.add_column("Y", justify="right")

    for idx, (x, y) in enumerate(centros_celdas):
        table.add_row(f"BS {idx}", f"{x:.2f}", f"{y:.2f}")

    console = Console()
    console.print(table)


def mostrar_usuarios_bs0(
    usuarios,              # lista de tuplas (x, y)
    matriz_potencias,      # lista de lista de dicts
    asignaciones,          # lista de índices de BS asignadas
    sirs,                  # lista de SIRs
    resultados_cqi,        # lista de dicts con CQI, eficiencia, tasa
    limite=10
):
    table = Table(title="[bold green]Usuarios asociados a BS0 (primeros 10)[/bold green]")
    table.add_column("ID", justify="center")
    table.add_column("X", justify="right")
    table.add_column("Y", justify="right")
    
    for bs_idx in range(len(matriz_potencias[0])):
        table.add_column(f"Loss BS{bs_idx}", justify="right")

    table.add_column("SIR (dB)", justify="right")
    table.add_column("CQI", justify="center")
    table.add_column("Eff. Esp.", justify="right")

    console = Console()

    count = 0
    for i, bs_asignada in enumerate(asignaciones):
        if bs_asignada == 0:
            x, y = usuarios[i]
            row = [str(i + 1), f"{x:.2f}", f"{y:.2f}"]

            # Añadir pérdidas hacia cada BS
            for bs_data in matriz_potencias[i]:
                row.append(f"{bs_data['loss_d']:.2f}")

            # Añadir SIR, CQI y eficiencia
            row.append(f"{sirs[i]:.2f}")
            row.append(str(resultados_cqi[i]["CQI"]))
            row.append(f"{resultados_cqi[i]['eficiencia']:.2f}")

            table.add_row(*row)

            count += 1
            if count >= limite:
                break

    console.print(table)

