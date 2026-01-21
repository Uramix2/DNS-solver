import dns.resolver
from concurrent.futures import ThreadPoolExecutor

def check_subdomain(full_domain):
    """Vérifie si un domaine complet existe."""
    resolver = dns.resolver.Resolver()
    
    try:
       
        resolver.resolve(full_domain, 'A')
        return full_domain
    except:
        try:
            resolver.resolve(full_domain, 'AAAA')
            return full_domain
        except:
            return None


def subdomain(domain, liste, threads=20):
    """
    Énumération simplifiée des sous-domaines.
    """
    targets = [f"{sub}.{domain}" for sub in liste]
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(check_subdomain, targets)) #  map lance des tâches en parallèle

        return [r for r in results if r]


if __name__ == "__main__":
    print(subdomain("oteria.fr", ["www", "grid", "ftp", "test", "dev", "api", "blog", "shop"],threads=10))
