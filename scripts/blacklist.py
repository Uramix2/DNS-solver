
with open("wordlists/blacklist.txt", "r") as f:
    liste = [line.strip() for line in f]


def is_blacklisted(domain):
    """
    Vérifie si un domaine est dans la liste noire.
    """
    for e in liste:
        if domain.endswith(e):
            return True
    return False

if __name__ == "__main__":
    print(is_blacklisted("cloudflare.net"))  
