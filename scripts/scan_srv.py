import dns.resolver

def scan_srv(domain, srv_list):
    """
    Scan les enregistrements SRV pour un domaine donné en utilisant une liste de noms SRV.
    """
    resolver = dns.resolver.Resolver()
    results = []
    
    for e in srv_list:
        test = f'{e}.{domain}'
        try:
            res = resolver.resolve(test, 'SRV')
            for r in res:
                clean_target = str(r.target).rstrip('.')
                results.append((clean_target, e))
        except Exception:
            continue
            
    return results


if __name__ == "__main__":
    print(scan_srv("se.com"))

