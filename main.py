from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from scripts.parser import parse_args
from scripts.brute_force_script import dns_type
from scripts.affichage import display_result

with open("wordlists/dns_types.txt","r") as data:
    liste = [line.strip() for line in data]

def main():
    args = parse_args()
    domain= args.domain
    console = Console()

    console.print(Panel(
            f"[bold blue]Liste les types et les informations trouvés pour le domaine [underline]{domain}[/underline][/bold blue]",
            title="DNS tools",
            border_style="blue",
            padding=(1, 2),
        ))
    
    result = dns_type(domain,liste,verbose=args.verbose)

    if result:
        display_result(domain,result,console)
    
    else:
        console.print("[red]domaine invalide[/red]")
            

if __name__ == "__main__":
    main()








            

    





