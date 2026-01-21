import ipaddress
from .scan import *
from .reverse_dns import revserse_dns
from .subdomain import subdomain, liste as subdomain_liste
from .scan_ip_neighbors import ip_neighbors
from .parser_txt import parse_txt, parent_domain
from .scan_srv import scan_srv 
from .blacklist import is_blacklisted

def is_ip(value):
    try:
        ipaddress.ip_address(str(value))
        return True
    except:
        return False

def clean(value):
    if not value: 
        return ""
    # Nettoie les points finaux et récupère le dernier segment (utile pour DNS)
    return str(value).strip().rstrip('.').split()[-1]

def scan_all(target, current_depth, visited, args, root_domain=None):
    small_subdomain = ["www", "mail", "remote", "blog", "webmail", "server", "ns1", "ns2", "smtp", "admin"]

    if visited is None:
        visited = set()
    
    target = clean(target)
    
    # Sécurités de base
    if not target or current_depth >= args.max_depth:
        return []
    
    # Définition du domaine racine pour limiter le brute-force
    if root_domain is None:
        root_domain = parent_domain(target) if not is_ip(target) else target

    # Blacklist et anti-boucle
    if target != root_domain and is_blacklisted(target):
        return []
    
    if target in visited:
        return []
    
    # Feedback visuel simple (remplace tqdm)
    print(f"    [>] Scanning: {target} ", end="\r")
    
    visited.add(target)
    results = []
    next_depth = current_depth + 1

    # --- LOGIQUE POUR LES ADRESSES IP ---
    if is_ip(target):
        # Voisins IP
        if args.scan_IP_neighbors:
            neighbors = ip_neighbors(target, size=args.ip_neighbors_size)
            if neighbors:
                valid_nbors = [clean(n) for n in neighbors if "Error" not in str(n)]
                if valid_nbors:
                    results.append(("NEIGHBORS", target, valid_nbors))
                    for n in valid_nbors:
                        results.extend(scan_all(n, next_depth, visited, args, root_domain))

        # Reverse DNS
        if args.reverse_DNS:
            rev = revserse_dns(target)
            if rev and "Error" not in str(rev):
                rev_c = clean(rev)
                results.append(("REVERSE", target, [rev_c]))
                results.extend(scan_all(rev_c, next_depth, visited, args, root_domain))

    # --- LOGIQUE POUR LES DOMAINES ---
    else:
        # Enregistrements DNS standards
        for nom, func in [("A", scan_a), ("MX", scan_mx), ("NS", scan_ns), ("CNAME", scan_cname), ("AAAA", scan_aaaa), ("PTR", scan_ptr)]:
            records = func(target)
            if records:
                valeurs = [clean(r) for r in records]
                results.append((nom, target, valeurs))
                
                for v in valeurs:
                    v_clean = clean(v)
                    # Détection de domaines externes
                    v_p = parent_domain(v_clean)
                    if v_p and v_p != root_domain and not is_ip(v_clean):
                        results.append(("EXT_DOMAIN", v_clean, [v_p]))
                    
                    results.extend(scan_all(v_clean, next_depth, visited, args, root_domain))

        # Analyse TXT (SPF, DKIM, etc.)
        if args.TXT_parser:
            txt_data = parse_txt(target)
            if isinstance(txt_data, dict):
                # ICI : On envoie le dictionnaire COMPLET (avec raw, emails...) au rendu
                results.append(("TXT_ANALYSIS", target, txt_data))
                
                # Récursion sur les domaines trouvés dans le TXT
                for d in txt_data.get("domains", []):
                    d_c = clean(d)
                    results.append(("TXT_LINK", target, [d_c]))
                    results.extend(scan_all(d_c, next_depth, visited, args, root_domain))
                
                # Récursion sur les IP trouvées dans le TXT
                for ip in txt_data.get("ipv4", []) + txt_data.get("ipv6", []):
                    results.append(("TXT_IP", target, [ip]))
                    results.extend(scan_all(ip, next_depth, visited, args, root_domain))

        # Scan SRV
        if args.scan_SRV:
            srv_records = scan_srv(target) 
            if srv_records:
                srv_targets = [clean(s[0]) for s in srv_records]
                results.append(("SRV", target, srv_targets))
                for st in srv_targets:
                    results.extend(scan_all(st, next_depth, visited, args, root_domain))

        # Énumération de sous-domaines (Brute-force)
        if args.subdomain_enum and root_domain in target:
            threads = getattr(args, 'threads', 20)
            current_wordlist = subdomain_liste if target == root_domain else small_subdomain
        
            subs = subdomain(target, current_wordlist, threads=threads)
            if subs:
                clean_subs = [clean(s) for s in subs]
                results.append(("SUB_BRUTE", target, clean_subs))
                for s in clean_subs:
                    results.extend(scan_all(s, next_depth, visited, args, root_domain))

    return results