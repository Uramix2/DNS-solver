import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="DNS Recon Tool")
    
    # target
    target_group = parser.add_argument_group("Target Configuration")
    target_group.add_argument("domain", help="Target domain")
    target_group.add_argument("-d", "--max-depth", type=int, default=2, help="Recursion depth (default: 2)")
    target_group.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")

    # SCAN
    special_group = parser.add_argument_group("Scans")
    special_group.add_argument("-txt", action="store_true", dest="TXT_parser", help="Parse TXT/SPF")
    special_group.add_argument("-r", "--rev", action="store_true", dest="reverse_DNS", help="Reverse DNS")
    special_group.add_argument("-i", "--neighbors", action="store_true", dest="scan_IP_neighbors", help="IP Neighbors")
    special_group.add_argument("-e", "--enum", action="store_true", dest="subdomain_enum", help="Subdomain enum")
    special_group.add_argument("-srv", "--srv", action="store_true", dest="scan_SRV", help="Scan SRV records")
    special_group.add_argument("-a", "--all", action="store_true", help="Enable all scans")

    # DNS Records Scans
    dns_group = parser.add_argument_group("DNS Records Scans")
    dns_group.add_argument("-sMX", action="store_true", dest="sMX", help="Scan MX records")
    dns_group.add_argument("-sNS", action="store_true", dest="sNS", help="Scan NS records")
    dns_group.add_argument("-sA", action="store_true", dest="sA", help="Scan A records")
    dns_group.add_argument("-sAAAA", action="store_true", dest="sAAAA", help="Scan AAAA records")
    dns_group.add_argument("-sCNAME", action="store_true", dest="sCNAME", help="Scan CNAME records")
    dns_group.add_argument("-sPTR", action="store_true", dest="sPTR", help="Scan PTR records")
    
    # Mini-Scan (Brute force Types on main domain only)
    dns_group.add_argument("-mini", "--mini-scan", action="store_true", dest="mini_scan", help="Mini Scan (Brute-force types on root only)")

    # output
    output_group = parser.add_argument_group("Output")
    output_group.add_argument("-w", "--wordlist", default="wordlists/liste_subdomains.txt")
    output_group.add_argument("--srv-wordlist", default="wordlists/SRV_name.txt")
    output_group.add_argument("--bf-wordlist", default="wordlists/dns_types.txt")
    output_group.add_argument("-s", "--size", type=int, default=2, dest="ip_neighbors_size", help="IP neighbors range")
    output_group.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    output_group.add_argument("-rep", "--report", action="store_true", help="Generate Markdown report")
    args = parser.parse_args()

    
    if args.mini_scan:
        args.all = False
        # Désactivation de tous les autres scans 
        for attr in ['sMX', 'sNS', 'sA', 'sAAAA', 'sCNAME', 'sPTR', 
                     'TXT_parser', 'reverse_DNS', 'scan_IP_neighbors', 'subdomain_enum', 'scan_SRV']:
            setattr(args, attr, False)
        return args

    dns = ['sMX', 'sNS', 'sA', 'sAAAA', 'sCNAME', 'sPTR']
    others = ['TXT_parser', 'reverse_DNS', 'scan_IP_neighbors', 'subdomain_enum', 'scan_SRV']
    
    # Accès direct au dictionnaire de l'objet args
    p = vars(args)

    # Pour --all
    if p['all']:
        for f in dns + others:
            p[f] = True

    # Si aucun type DNS n'est activé, on active tous les types DNS par défaut
    has_active_dns = False
    for t in dns:
        if p[t]:
            has_active_dns = True
            break
    # Si aucun type DNS n'est activé    
    if not has_active_dns:
        for t in dns:
            p[t] = True

    return args