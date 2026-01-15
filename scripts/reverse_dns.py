from dns import reversename

def revserse_dns(ip_address):
    """
    Pemet d'effectuer une recherche DNS inversée pour une adresse IP donnée
    """
    try :
        reverse_domain = reversename.from_address(ip_address)

    except Exception as e:
        return "Error : " + str(e)

    return reverse_domain


# -- test --
#print(revserse_dns("8.8.8.8"))



