import ipaddress
import re

from .scan import *
from .reverse_dns import revserse_dns
from .subdomain import subdomain, liste as subdomain_liste
from .scan_ip_neighbors import ip_neighbors


def is_ip(value):
    """Vérifie si une valeur est une adresse IP."""
    try:
        ipaddress.ip_address(str(value))
        return True
    except:
        return False
    

    
def expand_cidr(cidr):
    """Transforme un CIDR (192.168.1.0/30) en liste d'IPs."""
    try:
        return [str(ip) for ip in ipaddress.IPv4Network(cidr, strict=False)]
    except:
        return []


def clean(value):
    """Nettoie une valeur DNS."""
    parts = str(value).strip().rstrip('.').split()
    return parts[-1].rstrip('.')  # Prend la dernière partie (utile pour MX: "10 mail.domain.com")



def scan_all(target, current_depth, visited, args, root_domain=None):
    if visited is None:
        visited = set()
    
    # obj : définir le domaine racine 
    if root_domain is None:
        root_domain = target

    target = clean(target)
    if current_depth > args.max_depth or target in visited:
        return []
    
    visited.add(target)
    results = []

   
    if is_ip(target):
    
        rev = revserse_dns(target)
        if rev and "Error" not in str(rev):
            rev = clean(rev)
            results.append(("REVERSE", target, [rev]))
            results.extend(scan_all(rev, current_depth + 1, visited, args, root_domain=root_domain))
        
   
        neighbors = ip_neighbors(target, size=args.ip_neighbors_size)
        if neighbors:

            valid_neighbors = [n for n in neighbors if "Error" not in n] # filtrer les erreurs

            if valid_neighbors:
                results.append(("NEIGHBORS", target, valid_neighbors))


                for n in valid_neighbors:
                    results.extend(scan_all(n, current_depth + 1, visited, args, root_domain=root_domain))
  
    else:
    
        for nom, func in [("A", scan_a), ("MX", scan_mx), ("NS", scan_ns), ("CNAME", scan_cname)]:
            records = func(target)
            if records:
                valeurs = [clean(r) for r in records]
                results.append((nom, target, valeurs))
                for v in valeurs:
                    results.extend(scan_all(v, current_depth + 1, visited, args, root_domain=root_domain))
        if args.scan_SRV:
            srvs = scan_srv(target)
            if srvs:
                # On formate pour garder la cohérence (Nom, Cible, [Valeurs])
                srv_targets = [s[0] for s in srvs] 
                results.append(("SRV", target, srv_targets))
                for st in srv_targets:
                    results.extend(scan_all(st, current_depth + 1, visited, args, root_domain=root_domain))

        if args.TXT_parser:
            txt_records = scan_txt(target)
            if txt_records and not isinstance(txt_records, str):
                for t in txt_records:
                    # Ces boucles sont maintenant bien DANS la boucle 'for t'
                    for inc in re.findall(r'include:([^\s"]+)', str(t)):
                        results.extend(scan_all(clean(inc), current_depth + 1, visited, args, root_domain=root_domain))
                
                    for block in re.findall(r'ip[46]:([^\s"]+)', str(t)):
                        ips = expand_cidr(block)
                        for ip in ips[:3]: 
                            results.extend(scan_all(ip, current_depth + 1, visited, args, root_domain=root_domain))

            if args.subdomain_enum and root_domain in target:
                subs = subdomain(target, subdomain_liste)
                if subs:
                    results.append(("SUB_BRUTE", target, subs))
                    for s in subs:
                        results.extend(scan_all(s, current_depth + 1, visited, args, root_domain=root_domain))
    return results

