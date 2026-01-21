from scripts.parser import parse_args
from scripts.recursivite import scan_all
from scripts.graph import generate_graph
from scripts.rendu import generate_markdown

def main():
    args = parse_args()
    
    # Activation de toutes les options si --all est présent
    if args.all:
        args.TXT_parser = True
        args.scan_SRV = True
        args.reverse_DNS = True
        args.scan_IP_neighbors = True
        args.subdomain_enum = True

    print(f"[*] Scanning: {args.domain} (Max Depth: {args.max_depth})")
    
    visited = set()
    
    # Lancement du scan
    # Important : On peut aussi passer args.domain comme root_domain initial pour éviter le None
    results = scan_all(args.domain, 0, visited, args, root_domain=args.domain)

    if results:
        print(f"\n[+] Discovery finished: {len(visited)} nodes found, {len(results)} relations identified.")
        
        # 1. Génération du Graphe
        output_name = f"graph_{args.domain.replace('.', '_')}"
        generate_graph(results, output_name)
        print(f"[+] Graph saved: {output_name}.svg")
        
        # 2. Génération du Rapport HTML
        if getattr(args, 'report', False):
            report_file = generate_markdown(results, args.domain, visited)
            print(f"[+] Report generated: {report_file}")
            
    else:
        print("\n[!] No results found.")

if __name__ == "__main__":
    main()