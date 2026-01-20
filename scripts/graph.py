from graphviz import Digraph



def generate_graph(results, filename="dns_map"):
    dot = Digraph(comment='DNS Recon Map', format='svg')
     
    dot.attr(rankdir='TB')  # Graph vertical
    dot.attr(nodesep='0.7')
    dot.attr(ranksep='1.2')
    
    styles = {
        "A": {"color": "#2ecc71", "style": "solid"},
        "MX": {"color": "#e74c3c", "style": "dashed"},
        "NS": {"color": "#3498db", "style": "solid"},
        "REVERSE": {"color": "#9b59b6", "style": "dotted"},
        "NEIGHBORS": {"color": "#95a5a6", "style": "dotted"},
        "CNAME": {"color": "#f1c40f", "style": "solid"},
        "SUB_BRUTE": {"color": "#34495e", "style": "solid"},
        "TXT_DOM": {"color": "#e67e22", "style": "dashed"},
        "EXT_DOMAIN": {"color": "#c0392b", "style": "bold"} # Rouge gras pour les domaines parents
    }

    for type_res, source, targets in results:
        # Noeud Source
        s_shape = "box" if any(c.isalpha() for c in source) else "ellipse"
        dot.node(source, source, shape=s_shape, style="filled", fillcolor="#f8f9fa")

        for target in targets:
            # Noeud Cible
            t_shape = "box" if any(c.isalpha() for c in target) else "ellipse"
            dot.node(target, target, shape=t_shape)
            
            # config personnalisé
            config = styles.get(type_res, {"color": "black", "style": "solid"}) # par défaut noir solide
            dot.edge(source, target, label=type_res, color=config["color"], style=config["style"]) # lien personnalisé

    dot.render(filename, cleanup=True) # génère le fichier et supprime le .dot temporaire
