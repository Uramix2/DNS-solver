import ipaddress

from .reverse_dns import revserse_dns 

def ip_neighbors(ip_address, size=2):
    """
    Une adresse IP est entourée d'autres adresses IP. Parfois deux IP consécutive sont
    attribuées à deux machines de la même société.
    """
    liste = []

    for i in range(-size,size+1):
        # ici on évite l'IP de base
        if i == 0:
            continue 
        try:
            ip_neighbors = ipaddress.ip_address(ip_address) + i # pour avoir les IP voisines
            liste.append(str(revserse_dns(ip_neighbors)))

        except ValueError:
            continue

    return liste    

if __name__ == "__main__":
   
    print(ip_neighbors("92.61.160.137",2))




    

    

    