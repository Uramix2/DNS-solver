from scripts.parser import parse_args
from scripts.brute_force_script import dns_type
from scripts.affichage import display_result
from scripts.recursivite import scan_all

from scripts.scan import *
from scripts.graph import generate_graph


with open("wordlists/dns_types.txt","r") as data:
    liste = [line.strip() for line in data]


def main():
    args = parse_args()
    if args.all:
        args.TXT_parser = True
        args.scan_SRV = True
        args.reverse_DNS = True
        args.scan_IP_neighbors = True
        args.subdomain_enum = True

    print(f"[*] Scanning: {args.domain} (Depth: {args.max_depth})")
    
    visited = set()
    results = scan_all(args.domain, 0, visited, args, root_domain=None)  
     
    if results:
        print(f"[*] Generating graph with {len(results)} relations...")
        generate_graph(results, f"graph_{args.domain.replace('.', '_')}")
    else:
        print("[!] No results to graph.")

if __name__ == "__main__":
    main()

            

    





