import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("domain")
    parser.add_argument("-t","--TXT-parser", action="store_true", help="Analyse récursivement les enregistrements TXT pour extraire des informations supplémentaires")
    parser.add_argument("-b","--brute-force", action="store_true", help="Effectue une recherche brute force des types DNS pour un domaine donné")
    parser.add_argument("-v", "--verbose", action="store_true", help="Affiche les erreurs rencontrées lors de la résolution DNS")
    parser.add_argument("-s","--scan-SRV", action="store_true", help="Scanne les enregistrements SRV pour un domaine donné")
    parser.add_argument("-r","--reverse-DNS", action="store_true", help="Effectue une recherche DNS inversée pour une adresse IP donnée")
    parser.add_argument("-i","--scan-IP-neighbors", action="store_true", help="Scanne les adresses IP voisines dans un sous-réseau donné")
    parser.add_argument("-e","--subdomain-enum", action="store_true", help="Effectue une énumération des sous-domaines pour un domaine donné")
    parser.add_argument("-d","--max-depth", type=int, default=2, help="Profondeur maximale pour l'analyse récursive des enregistrements TXT (par défaut: 2)")
    parser.add_argument("-a","--all", action="store_true", help="Exécute toutes les fonctionnalités disponibles sauf brute force")
    parser.add_argument("--tld", action="store_true", help="Récupère les domaines parents")
    return parser.parse_args()
