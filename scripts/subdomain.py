import dns.resolver
from multiprocessing import Pool


with open("wordlists/liste_subdomains.txt", "r") as f:
    liste = [line.strip() for line in f]

def subdomain(domain,liste):
    """
    Enumération des sous-domaines pour un domaine donné en utilisant une liste de mots.
    Retourne une liste des sous-domaines trouvés.
    """
    found_subdomains = []
    resolver = dns.resolver.Resolver()
    for subdomain in liste:
        full_domain = f"{subdomain}.{domain}"
        try:
            answers = resolver.resolve(full_domain, 'A') 
            if answers:
                found_subdomains.append(full_domain)
        except:
            try:
                answers = resolver.resolve(full_domain, 'AAAA')
                if answers:
                    found_subdomains.append(full_domain)

            except:
                continue
        

    return found_subdomains


if __name__ == "__main__":
    # -- test --
    print(subdomain("tf1.fr", liste))
