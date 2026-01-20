import ipaddress


from .scan import *
from .reverse_dns import revserse_dns
from .subdomain import subdomain, liste as subdomain_liste
from .scan_ip_neighbors import ip_neighbors
from .parser_txt import parse_txt, parent_domain
from .scan_srv import scan_srv 

# paramètre pour limiter la taille du graphe
MAX_VISITED = 1000
MAX_TARGETS_PER_RECORD = 25


def is_ip(value):
    try:
        ipaddress.ip_address(str(value))
        return True
    except:
        return False
    


def clean(value):
    if not value: 
        return ""
    return str(value).strip().rstrip('.').split()[-1] # enlver les espaces,pointspour avoir seulemnt le domaine/IP



def scan_all(target, current_depth, visited, args, root_domain=None):
    """
    Fonction récursive pour scanner un domaine ou une IP et explorer les résultats.
    Elle gère la profondeur maximale, évite les cycles et collecte les résultats. Pour les envoyer au graphe.
    """
    if visited is None:
        visited = set()
    
    target = clean(target) 
    if not target or current_depth > args.max_depth: 
        return []


    visit_id = f"{'IP' if is_ip(target) else 'DNS'}:{target}"
    if visit_id in visited:
        return []
    
    visited.add(visit_id)
    
    
    if root_domain is None:
        root_domain = parent_domain(target) if not is_ip(target) else target

    results = []

    if is_ip(target):
        #  SCAN VOISINS IP 
        if args.scan_IP_neighbors:
            neighbors = ip_neighbors(target, size=args.ip_neighbors_size) 
            if neighbors:
                valid_neighbors = [clean(n) for n in neighbors if "Error" not in n]

                if valid_neighbors:
                    results.append(("NEIGHBORS", target, valid_neighbors))

                    # Récursion sur les voisins trouvés
                    for n in valid_neighbors:
                        results.extend(scan_all(n, current_depth + 1, visited, args, root_domain))

        # REVERSE DNS 
        rev = revserse_dns(target) 

        if rev and "Error" not in str(rev):
            rev = clean(rev)
            results.append(("REVERSE", target, [rev]))
            results.extend(scan_all(rev, current_depth + 1, visited, args, root_domain))

    else:
        # DOMAINE (A, MX, NS, TXT,CNAME) 
        for nom, func in [("A", scan_a), ("MX", scan_mx), ("NS", scan_ns), ("CNAME", scan_cname)]:
            records = func(target) 

            if records:
                valeurs = [clean(r) for r in records]
                results.append((nom, target, valeurs))

                for v in valeurs:
                    v_clean = clean(v)
                    # Si c'est un domaine externe (ex: google.com), on crée le lien parent
                    p = parent_domain(v_clean)

                    if p and p != root_domain and not is_ip(v_clean):
                        results.append(("EXT_DOMAIN", v_clean, [p]))
                    
                    results.extend(scan_all(v_clean, current_depth + 1, visited, args, root_domain))

        # SCAN TXT (IPs et Domaines)
        if args.TXT_parser:
            txt_data = parse_txt(target) 
            if isinstance(txt_data, dict):
                
                # Domaines dans le TXT  
                for d in txt_data.get("domains", []):
                    d_c = clean(d)
                    results.append(("TXT_DOM", target, [d_c]))
                    p = parent_domain(d_c)

                    if p and p != root_domain:
                        results.append(("EXT_DOMAIN", d_c, [p]))
                    results.extend(scan_all(d_c, current_depth + 1, visited, args, root_domain))

                # IPs dans le TXT
                for ip in txt_data.get("ipv4", []):
                    results.append(("TXT_IP", target, [ip]))
                    results.extend(scan_all(ip, current_depth + 1, visited, args, root_domain))

        #SUBDOMAINS 
        if args.subdomain_enum and root_domain in target:
            subs = subdomain(target, subdomain_liste) 

            if subs:
                results.append(("SUB_BRUTE", target, subs))

                for s in subs:
                    results.extend(scan_all(s, current_depth + 1, visited, args, root_domain))

    return results

if __name__ == "__main__":
   
    args = lambda: None
    args.max_depth = 2
    args.scan_IP_neighbors = True
    args.TXT_parser = True
    args.subdomain_enum = True
    args.scan_SRV = False

    visited = set()
    results = scan_all("oteria.fr", 0, visited, args)
    for res in results:
        print(res)