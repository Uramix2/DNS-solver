from dns import reversename
import dns.resolver

def revserse_dns(ip_address):
    """
    Effectue une recherche DNS inversée pour une adresse IP donnée.
    Retourne le nom de domaine associé ou un message d'erreur.
    """
    try:
        # string 
        ip_str = str(ip_address)
        reverse_name = reversename.from_address(ip_str)
        resolved_name = str(dns.resolver.resolve(reverse_name, "PTR")[0])
        return resolved_name
    
    except Exception as ex:
        return f"Error DNS with {ip_address}"

if __name__ == "__main__":
    print(revserse_dns("34.227.236.7"))

