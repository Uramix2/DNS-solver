from graphviz import Digraph

def generate_graph(results, filename="dns_map"):
    dot = Digraph(comment='DNS Recon Map', format='svg')
    dot.attr(rankdir='TB', nodesep='0.7', ranksep='1.2')
    
    styles = {
        "A": {"color": "#2ecc71", "style": "solid"},
        "AAAA": {"color": "#27ae60", "style": "solid"},
        "PTR": {"color": "#8e44ad", "style": "dotted"},
        "MX": {"color": "#e74c3c", "style": "dashed"},
        "NS": {"color": "#3498db", "style": "solid"},
        "REVERSE": {"color": "#9b59b6", "style": "dotted"},
        "NEIGHBORS": {"color": "#95a5a6", "style": "dotted"},
        "CNAME": {"color": "#f1c40f", "style": "solid"},
        "SUB_BRUTE": {"color": "#34495e", "style": "solid"},
        "TXT_DOM": {"color": "#e67e22", "style": "dashed"},
        "EXT_DOMAIN": {"color": "#c0392b", "style": "bold"}, 
        "SRV": {"color": "#1abc9c", "style": "dashed"},
    }

    created_nodes = set()

    for type_res, source, targets in results:
       # corriger le pb lié aux guillemets dans les ipv6
        s_label = str(source).strip().replace('"', '')
        s_id = s_label.replace(':', '_') 
        
        if s_id not in created_nodes:
            s_shape = "box" if any(c.isalpha() for c in s_label) else "ellipse"
            dot.node(s_id, label=s_label, shape=s_shape, style="filled", fillcolor="#f8f9fa")
            created_nodes.add(s_id)

        for target in targets:
            # corriger le pb lié aux guillemets dans les ipv6
            t_label = str(target).strip().replace('"', '')
            t_id = t_label.replace(':', '_')
            
            if t_id not in created_nodes:
                t_shape = "box" if any(c.isalpha() for c in t_label) else "ellipse"
                dot.node(t_id, label=t_label, shape=t_shape)
                created_nodes.add(t_id)
            
            config = styles.get(type_res, {"color": "black", "style": "solid"}) 
            dot.edge(s_id, t_id, label=str(type_res), color=config["color"], style=config["style"])

    dot.render(filename, cleanup=True)