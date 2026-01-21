import dns.resolver
import re

def parse_txt(domain):
    """
    Analyse les enregistrements TXT pour extraire domaines, emails, IPv4 et IPv6.
    """
    resolver = dns.resolver.Resolver()
    
    # regex patterns pour le domaine, email, IPv4 et IPv6
    domain_regex = re.compile(r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}')
    email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    ipv4_regex = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    ipv6_regex = re.compile(r'(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}')

    found_info_dico = {
        "raw": [],
        "domains": [],
        "emails": [],
        "ipv4": [],
        "ipv6": []
    }

    try:
        response = resolver.resolve(domain, 'TXT')
        for record in response:
            str_e = str(record).replace('"', '')
            found_info_dico["raw"].append(str_e)

            found_info_dico["domains"].extend(domain_regex.findall(str_e))
            found_info_dico["emails"].extend(email_regex.findall(str_e))
            found_info_dico["ipv4"].extend(ipv4_regex.findall(str_e))
            found_info_dico["ipv6"].extend(ipv6_regex.findall(str_e))
    

    except dns.resolver.NoAnswer:
        return f'No TXT record found for {domain}'
    
    except Exception as ex:
        return f"Error: {ex}"
            
    return found_info_dico



def parent_domain(domain):
    """
    Retourne le domaine parent d'un domaine donné.
    Exemple : pour "sub.example.com", retourne "example.com".
    """
    parts = domain.split('.')
    if len(parts) < 2:
        return None  
    return '.'.join(parts[-2:]) 



def TLD(domain):
    """
    Permet de lister touts les TLD d'un domaine donné
    """
    domain_parts = domain.split('.')
    tlds = []
    for i in range(1, len(domain_parts) - 1):
        tld = '.'.join(domain_parts[i:])
        if parent_domain(tld) != tld:
            tlds.append(tld)
    return tlds
    



if __name__ == "__main__":
    print(parse_txt("oteria.fr"))
    print(TLD("sirena.integration.dev.atlas.fabrique.social.gouv.fr"))
    print(parent_domain("sub.example.com"))

