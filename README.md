# DNS Solver

DNS Solver est un scanner de reconnaissance DNS avancé écrit en Python. Il permet d'explorer récursivement l'infrastructure DNS d'un domaine cible, de découvrir des sous-domaines, d'analyser les relations entre les enregistrements et de présenter les résultats sous forme de graphes et de rapports détaillés.

## Description

Le projet a pour but d'automatiser la phase de reconnaissance passive et active sur un nom de domaine. Il interroge différents types d'enregistrements DNS, analyse les réponses et utilise ces nouvelles informations pour étendre la surface d'analyse (récursivité).

## Fonctionnalités Principales

- **Résolution DNS** : Interrogation des enregistrements A, AAAA, CN, MX, NS, PTR, SRV et TXT.
- **Mode Récursif** : Exploration automatique des nouvelles cibles (domaines et IPs) découvertes jusqu'à une profondeur définie.
- **Analyse TXT Avancée** : Extraction automatique d'IPv4, IPv6 et de noms de domaine présents dans les enregistrements TXT.
- **Découverte de Sous-domaines** : Énumération par dictionnaire (brute-force) utilisant le multi-threading pour la performance.
- **Voisinage IP** : Recherche inversée sur les adresses IP adjacentes pour trouver d'autres domaines hébergés sur la même plage.
- **Visualisation Graphique** : Génération de diagrammes relationnels vectoriels (SVG) via Graphviz.
- **Rapports** : Export des résultats au format HTML structuré pour une analyse ultérieure.

## Installation

### Installation Rapide

Pour utiliser toutes les fonctionnalités de scan et de rapport, seule l'installation des dépendances Python est nécessaire :

```bash
git clone <url_du_repo>
cd projet_dns
pip install -r requirements.txt
```

### Prérequis Optionnel (Pour les Graphes)

Si vous souhaitez utiliser l'option `--graph` pour visualiser les résultats :
- Le logiciel **Graphviz** doit être installé sur votre machine (et ajouté au PATH).
  - **Linux** : `sudo apt install graphviz`
  - **Windows** : `choco install graphviz` ou via l'installeur officiel.

*Note : Si Graphviz n'est pas installé, tout fonctionnera sauf la génération des fichiers .svg.*

## Utilisation

L'outil s'utilise en ligne de commande via le script `main.py`.

### Syntaxe Générale

```bash
python main.py <domaine> [options]
```

### Options

| Option | Description |
|--------|-------------|
| **Cible & Configuration** | |
| `-d`, `--max-depth` | Profondeur de récursion maxi (défaut : 2). |
| `-t`, `--threads` | Nombre de threads pour le brute-force de sous-domaines (défaut : 10). |
| `-v`, `--verbose` | Mode verbeux. |
| **Modules de Scan** | |
| `-a`, `--all` | Active **TOUS** les scans (recommandé pour un audit complet). |
| `-mini`, `--mini-scan` | **Mode Exclusif** : Brute-force des types DNS sur la racine uniquement (désactive tout le reste). |
| `-srv`, `--srv` | Active le scan des enregistrements SRV. |
| `-txt` | Active l'analyse avancée des enregistrements TXT/SPF. |
| `-r`, `--rev` | Active la résolution inverse DNS (Reverse DNS). |
| `-i`, `--neighbors` | Active la recherche de voisins IP (Voisinage IP). |
| `-e`, `--enum` | Active l'énumération de sous-domaines par brute-force. |
| **Filtres Enregistrements** | (Si aucun spécifié, tous sont actifs par défaut sauf si -e ou -mini est utilisé) |
| `-sA` | Scan des enregistrements A. |
| `-sAAAA` | Scan des enregistrements AAAA. |
| `-sMX` | Scan des enregistrements MX. |
| `-sNS` | Scan des enregistrements NS. |
| `-sCNAME` | Scan des enregistrements CNAME. |
| `-sPTR` | Scan des enregistrements PTR. |
| **Entrées/Sorties** | |
| `-rep`, `--report` | Génère un rapport Markdown récapitulatif. |
| `-w` | Chemin vers la wordlist pour les sous-domaines. |
| `--srv-wordlist` | Chemin vers la wordlist pour les services SRV. |
| `--bf-wordlist` | Chemin vers la wordlist pour le bruteforce de types (Mode Mini). |

### Exemples d'exécution

**1. Scan complet standard :**

```bash
python main.py exemple.fr --all --report
```

**2. Mini-Scan (Brute-force des types DNS uniquement) :**

```bash
python main.py exemple.fr --mini-scan
```

**3. Scan de sous-domaines uniquement (Brute-force) :**

```bash
python main.py exemple.fr -e -t 50
```

**4. Scan sélectif (MX et NS uniquement) :**

```bash
python main.py exemple.fr -sMX -sNS
```

**5. Recherche approfondie :**

```bash
python main.py exemple.fr -a -d 3
```

*Note : Un graphe SVG est généré automatiquement à la fin du scan si des résultats sont trouvés (Nécessite Graphviz).*

## Structure du Projet

- `main.py` : Point d'entrée de l'application.
- `scripts/` : Modules fonctionnels (parsing, scans, récursivité, affichage).
- `wordlists/` : Dictionnaires utilisés pour l'énumération DNS.
- `tests/` : Tests unitaires.

## ⚠️ Avertissement

⚠️⚠️⚠️ Cet outil est destiné à des fins éducatives et d'audit légitime uniquement. L'utilisateur est responsable de l'utilisation qu'il en fait. Assurez-vous d'avoir l'autorisation de scanner les cibles visées.
