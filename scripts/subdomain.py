import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

with open("wordlists/liste_subdomains.txt", "r") as f:
    liste = [line.strip() for line in f]


def check_subdomain(args):
    """Vérifie si un sous-domaine existe (pour le multithread)."""
    subdomain_name, domain = args
    full_domain = f"{subdomain_name}.{domain}"
    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 2
    try:
        answers = resolver.resolve(full_domain, 'A')
        if answers:
            return full_domain
    except:
        try:
            answers = resolver.resolve(full_domain, 'AAAA')
            if answers:
                return full_domain
        except:
            pass
    return None


def subdomain(domain, liste, threads=20):
    """
    Enumération des sous-domaines pour un domaine donné en utilisant une liste de mots.
    Utilise le multithread pour accélérer la recherche.
    Retourne une liste des sous-domaines trouvés.
    """
    found_subdomains = []
    
    # Préparer les arguments pour chaque thread
    args = [(sub, domain) for sub in liste]
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_subdomain, arg): arg for arg in args}
        for future in as_completed(futures):
            result = future.result()
            if result:
                found_subdomains.append(result)
    
    return found_subdomains


if __name__ == "__main__":
    # -- test --
    print(subdomain("oteria.fr", liste))
