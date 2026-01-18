import dns.resolver
import re

def resolver(domain, record_type):
    """
    Résout un enregistrement DNS pour un domaine donné et un type d'enregistrement spécifié.
    Retourne une liste des valeurs résolues ou None en cas d'erreur.
    """
    resolver = dns.resolver.Resolver()
    try:
        answers = resolver.resolve(domain, record_type)
        values = [str(r) for r in answers]
        return values
    
    except Exception as ex:
        return 

def scan_a(domain):
    return resolver(domain,'A')

def scan_aaaa(domain):
    return resolver(domain,'AAAA')

def scan_mx(domain):
    return resolver(domain,'MX')

def scan_cname(domain):
    return resolver(domain,'CNAME')

def scan_ns(domain):
    return resolver(domain,'NS')

def scan_txt(domain):
    return resolver(domain,'TXT')

def scan_srv(domain):
    return resolver(domain,'SRV')

def scan_ptr(domain):
    return resolver(domain,'PTR')



