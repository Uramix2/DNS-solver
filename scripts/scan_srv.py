import dns.resolver



with open("wordlists/SRV_name.txt","r") as data:
    liste = [line.strip() for line in data]


def scan_srv(domain):
    """
    Scan les enregistrements SRV pour un domaine donné en utilisant une liste de noms SRV.
    """
    resolver = dns.resolver.Resolver()
    results = []
    for e in liste:
        test = f'{e}.{domain}'

        try:
            
            res = resolver.resolve(test, 'SRV')

            for r in res:
                clean  = str(r.target).rstrip('.')
                results.append((clean,e))
            
        except Exception:
            continue
    return results


if __name__ == "__main__":
    # -- test --
    print(scan_srv("se.com"))

