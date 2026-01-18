import ipaddress
import re

from scan import *
from reverse_dns import revserse_dns
from subdomain import subdomain, liste as subdomain_liste
from scan_ip_neighbors import ip_neighbors


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

def scan_all(target, depth_max, current_depth=0, visited=None,size=2, root_domain=None):
    if visited is None:
        visited = set()
    
    # obj : définir le domaine racine 
    if root_domain is None:
        root_domain = target

    target = clean(target)
    if current_depth > depth_max or target in visited:
        return []
    
    visited.add(target)
    results = []

   
    if is_ip(target):
    
        rev = revserse_dns(target)
        if rev and "Error" not in str(rev):
            rev = clean(rev)
            results.append(("REVERSE", target, [rev]))
            results.extend(scan_all(rev, depth_max, current_depth + 1, visited, root_domain=root_domain))
        
   
        neighbors = ip_neighbors(target, size=size)
        if neighbors:

            valid_neighbors = [n for n in neighbors if "Error" not in n] # filtrer les erreurs

            if valid_neighbors:
                results.append(("NEIGHBORS", target, valid_neighbors))


                for n in valid_neighbors:
                    results.extend(scan_all(n, depth_max, current_depth + 1, visited, size=size, root_domain=root_domain))
  
    else:
    
        for nom, func in [("A", scan_a), ("MX", scan_mx), ("NS", scan_ns), ("CNAME", scan_cname)]:
            records = func(target)
            if records:
                valeurs = [clean(r) for r in records]
                results.append((nom, target, valeurs))
                for v in valeurs:
                    results.extend(scan_all(v, depth_max, current_depth + 1, visited, size=size, root_domain=root_domain))

        txt_records = scan_txt(target)
        if txt_records and not isinstance(txt_records, str):
            for t in txt_records:

                for inc in re.findall(r'include:([^\s"]+)', str(t)):
                    results.extend(scan_all(clean(inc), depth_max, current_depth + 1, visited, size=size, root_domain=root_domain))
                
                for block in re.findall(r'ip[46]:([^\s"]+)', str(t)):
                    ips = expand_cidr(block)


                    for ip in ips[:3]: 
                        results.extend(scan_all(ip, depth_max, current_depth + 1, visited, size=size, root_domain=root_domain))

        if target == root_domain:
            subs = subdomain(target, subdomain_liste)
      
            if subs:
                results.append(("SUB_BRUTE", target, subs))
                for s in subs:
                    results.extend(scan_all(s, depth_max, current_depth + 1, visited, size=size, root_domain=root_domain))

    return results

if __name__ == "__main__":
    test = scan_all("oteria.fr", depth_max=2)
    for t in test:
        print(t)