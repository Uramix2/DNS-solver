from rich.table import Table
from rich.console import Console
from rich.panel import Panel

def display_result(domain,results,console):
    table = Table(
        title=f"Résultat pour {domain}",
        show_header=True,
        header_style="bold white on blue",
        border_style="bright_black",
        expand=True)
    
    table.add_column("Type",style="cyan")
    table.add_column("Valeurs",style="Green",overflow="fold")

    for types,val in results.items():
        table.add_row(types, "\n".join(val))
        table.add_section()
    

    console.print(table)
