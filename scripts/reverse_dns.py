from dns import reversename
import dns.resolver

def revserse_dns(ip_address):
    """
    Effectue une recherche DNS inversée pour une adresse IP donnée.
    Retourne le nom de domaine associé ou un message d'erreur.
    """
    liste = []
    try:
        reverse_name = reversename.from_address(ip_address).to_text().split(" ")[0]
        liste.append(reverse_name)
        resolved_name = str(dns.resolver.resolve(reverse_name, "PTR")[0])
        liste.append(resolved_name)
        return liste
    
    
    except Exception as ex:
        return f"Error with reverse DNS"

if __name__ == "__main__":
    # -- test --
    # assert revserse_dns("34.227.236.7") == "ec2-34-227-236-7.compute-1.amazonaws.com."
    print(revserse_dns("34.227.236.7"))

