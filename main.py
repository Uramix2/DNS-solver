from scripts.parser import parse_args
from scripts.brute_force_script import dns_type
from scripts.affichage import display_result
from scripts.recursivite import scan_all
from scripts.scan import *

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

    print(f"[*] Scanning: {args.domain}")
    
    # Lancement du scan
    visited = set()
    results = scan_all(args.domain, 0, visited, args)
    for type_res,source, targets in results:
        # On affiche uniquement la relation directe pour plus de clarté
        print(f"{type_res} -> {targets}")

if __name__ == "__main__":
    main()





            

    





