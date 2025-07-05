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
