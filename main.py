from scripts.parser import parse_args
from scripts.recursivite import scan_all
from scripts.graph import generate_graph
from scripts.rendu import generate_markdown

def main():
    args = parse_args()
    
    try:
        if args.subdomain_enum or args.all:
            with open(args.wordlist, "r") as f:
                args.subdomain_list = [line.strip() for line in f]
        
        if args.scan_SRV or args.all:
            with open(args.srv_wordlist, "r") as f:
                args.srv_list = [line.strip() for line in f]

        if getattr(args, 'mini_scan', False):
            with open(args.bf_wordlist, "r") as f:
                args.bf_list = [line.strip() for line in f]

    except FileNotFoundError as e:
        print(f"[!] Error loading wordlist: {e}")
        return

    # Activation de toutes les options si --all est présent
    if args.all:
        args.TXT_parser = True
        args.scan_SRV = True
        args.reverse_DNS = True
        args.scan_IP_neighbors = True
        args.subdomain_enum = True

    print(f"[*] Scanning: {args.domain} (Max Depth: {args.max_depth})")
    
    visited = set()
    

    results = scan_all(args.domain, 0, visited, args, root_domain=args.domain) # évite de scanner en dehors du domaine racine

    if results:
        print(f"\n[+] Discovery finished: {len(visited)} nodes found, {len(results)} relations identified.")
        
        #  Graphe
        output_name = f"graph_{args.domain.replace('.', '_')}"
        generate_graph(results, output_name)
        print(f"[+] Graph saved: {output_name}.svg")
        
        #  Rapport 
        if getattr(args, 'report', False):
            report_file = generate_markdown(results, args.domain, visited)
            print(f"[+] Report generated: {report_file}")
            
    else:
        print("\n[!] No results found.")

if __name__ == "__main__":
    main()