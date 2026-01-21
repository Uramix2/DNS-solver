import dns.resolver


def dns_type(domain, liste, verbose=False):
    """
    Permet d'afficher les types de dns via brute force
    """
    resolver = dns.resolver.Resolver()
    result = {}
    for e in liste:
        try:
            answers = resolver.resolve(domain, e)
            values = [str(r) for r in answers]
            if values:
                result[e] = values
        except Exception as ex:
            if verbose:
                print(e, "error : -->", type(ex).__name__)
            continue
    return result

if __name__ == "__main__":
    # -- test --
    with open("wordlists/dns_types.txt","r") as data:
        liste = [line.strip() for line in data]

    domain = "oteria.fr"
    res = dns_type(domain, liste, verbose=True)
    for k, v in res.items():
        print(f"{k} : {v}")





