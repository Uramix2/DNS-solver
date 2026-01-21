import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="DNS Recon Tool")
    
    parser.add_argument("domain", help="Target domain")
    
    parser.add_argument("-d", "--max-depth", type=int, default=2, help="Recursion depth (default: 2)")
    parser.add_argument("-s", "--size", type=int, default=2, dest="ip_neighbors_size", help="IP neighbors range")
    parser.add_argument("-w", "--wordlist", default="wordlists/liste_subdomains.txt")

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")

    parser.add_argument("-txt", action="store_true", dest="TXT_parser", help="Parse TXT/SPF")
    parser.add_argument("-r", "--rev", action="store_true", dest="reverse_DNS", help="Reverse DNS")
    parser.add_argument("-i", "--neighbors", action="store_true", dest="scan_IP_neighbors", help="IP Neighbors")
    parser.add_argument("-e", "--enum", action="store_true", dest="subdomain_enum", help="Subdomain enum")
    parser.add_argument("-srv", "--srv", action="store_true", dest="scan_SRV", help="Scan SRV records")
    parser.add_argument("-a", "--all", action="store_true", help="Enable all scans")
    parser.add_argument("-rep", "--report", action="store_true", help="Générer un rapport Markdown détaillé")

    args = parser.parse_args()

    if args.all:
        for funct in ['TXT_parser', 'reverse_DNS', 'scan_IP_neighbors', 'subdomain_enum', 'scan_SRV']:
            setattr(args, funct, True)
            
    return args