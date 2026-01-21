from scripts.parser import parse_args
from scripts.recursivite import scan_all
from scripts.graph import generate_graph

def main():
    args = parse_args()
    if args.all:
        args.TXT_parser = True
        args.scan_SRV = True
        args.reverse_DNS = True
        args.scan_IP_neighbors = True
        args.subdomain_enum = True

    print(f"[*] Scanning: {args.domain} (Max Depth: {args.max_depth})")
    
    visited = set()
   
    
    results = scan_all(args.domain, 0, visited, args, root_domain=None)
    

    if results:
        print(f"[+] Discovery finished: {len(visited)} nodes found, {len(results)} relations identified.")
        generate_graph(results, f"graph_{args.domain.replace('.', '_')}")
        print(f"[+] Graph saved: graph_{args.domain.replace('.', '_')}.svg")
    else:
        print("[!] No results to graph.")

if __name__ == "__main__":
    main()