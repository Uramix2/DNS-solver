import argparse
import dns.resolver
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

liste = [
    "A",
    "AAAA",
    "MX",
    "NS",
    "TXT",
    "SOA",
    "CNAME",
    "CAA",
    "PTR",
    "SRV",
    "DS",

    
]


def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("domain")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def dns_type(domain, liste,verbose=False):
    """
    Permet d'afficher les types de dns via brute force
    """
    resolver = dns.resolver.Resolver()
    resolver.lifetime = 3.0 #  2 secondes max par req
    result = {}
    for e in liste:
        try:
            answers = resolver.resolve(domain, e)
            values = [str(r) for r in answers]
            if values:
                result[e] = values
        except Exception as ex:
            if verbose:
                print(e, "error : -->", type(ex).__name__)
            continue
    return result


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








            

    





