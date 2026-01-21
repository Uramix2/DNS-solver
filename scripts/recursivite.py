import ipaddress
from .scan import *
from .reverse_dns import revserse_dns
from .subdomain import subdomain
from .scan_ip_neighbors import ip_neighbors
from .parser_txt import parse_txt, parent_domain
from .scan_srv import scan_srv 
from .brute_force_script import dns_type
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
    
    # conditions d'arrêt

    if visited is None: visited = set()
    target = clean(target)

    if not target or current_depth >= args.max_depth or target in visited:
        return []

    if root_domain is None:
        p_dom = parent_domain(target)
        root_domain = p_dom if p_dom else target

    if target != root_domain and is_blacklisted(target):
        return []

    #  MINI-SCAN 
    if getattr(args, 'mini_scan', False):
        print(f"    [>] Mini-Scan: {target} ", end="\r")
        visited.add(target)
        res = []
        found_types = dns_type(target, args.bf_list, verbose=args.verbose)
        
        for r_type in found_types:
            values = found_types[r_type]
            if values:
                cleaned_vals = [clean(v) for v in values]
                res.append((f"MINI_SCAN_{r_type}", target, cleaned_vals))
        return res # On s'arrête ici pour le mini-scan

    # SCAN COMPLET
    print(f"    [>] Scanning: {target} ", end="\r")
    visited.add(target)
    results = []
    next_depth = current_depth + 1

    # is IP
    if is_ip(target):
        # Reverse DNS
        if args.reverse_DNS:
            rev = revserse_dns(target)
            if rev and "Error" not in str(rev):
                rev_c = clean(rev)
                results.append(("REVERSE", target, [rev_c]))
                results.extend(scan_all(rev_c, next_depth, visited, args, root_domain))
        
        # Voisins IP
        if args.scan_IP_neighbors:
            nbors = ip_neighbors(target, size=args.ip_neighbors_size)
            if nbors:
                v_nbors = [clean(n) for n in nbors if "Error" not in str(n)]
                results.append(("NEIGHBORS", target, v_nbors))
                for n in v_nbors:
                    results.extend(scan_all(n, next_depth, visited, args, root_domain))

    # is domain
    else:
        # DNS Standards (A, MX, NS, CNAME, etc.)
        # liste des tuples (argument, label, fonction)
        records_to_check = [
            ('sA', 'A', scan_a), ('sMX', 'MX', scan_mx), 
            ('sNS', 'NS', scan_ns), ('sCNAME', 'CNAME', scan_cname),
            ('sAAAA', 'AAAA', scan_aaaa), ('sPTR', 'PTR', scan_ptr)
        ]

        for arg_flag, label, func in records_to_check:
            if getattr(args, arg_flag, False):
                found = func(target)

                if found:
                    cleaned_found = [clean(f) for f in found]
                    results.append((label, target, cleaned_found))

                    for f_val in cleaned_found:

                        f_p = parent_domain(f_val)

                        if f_p and f_p != root_domain and not is_ip(f_val):
                            results.append(("EXT_DOMAIN", f_val, [f_p]))
                        results.extend(scan_all(f_val, next_depth, visited, args, root_domain))

        # Analyse TXT
        if args.TXT_parser:
            txt = parse_txt(target)

            if type(txt) == dict:
                results.append(("TXT_ANALYSIS", target, txt))
                to_crawl = txt.get("domains", []) + txt.get("ipv4", []) + txt.get("ipv6", [])
                
                for item in to_crawl:
                    item_c = clean(item)
                    label = "TXT_IP" if is_ip(item_c) else "TXT_LINK"
                    results.append((label, target, [item_c]))
                    results.extend(scan_all(item_c, next_depth, visited, args, root_domain))

        # Scan SRV
        if args.scan_SRV:
            srvs = scan_srv(target, getattr(args, 'srv_list', []))

            if srvs:
                targets = [clean(s[0]) for s in srvs]
                results.append(("SRV", target, targets))

                for t in targets:
                    results.extend(scan_all(t, next_depth, visited, args, root_domain))

        # Sous-domaines (wordlist)
        if args.subdomain_enum and root_domain in target:
            wordlist = args.subdomain_list if target == root_domain else small_subdomain
            subs = subdomain(target, wordlist, threads=getattr(args, 'threads', 20))

            if subs:
                c_subs = [clean(s) for s in subs]
                results.append(("SUB_BRUTE", target, c_subs))
                
                for s in c_subs:
                    results.extend(scan_all(s, next_depth, visited, args, root_domain))

    return results