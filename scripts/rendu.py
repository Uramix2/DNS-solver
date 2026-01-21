from datetime import datetime

def generate_markdown(results, target_domain, visited_nodes):
    filename = f"report_{target_domain.replace('.', '_')}.html"
    heure_rapport = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # statistiques
    stats = {}
    for rtype, source, values in results:
        if rtype not in stats:
            stats[rtype] = 0
        stats[rtype] += 1
    
    # HTML des statistiques
    stats_html = ""
    for rtype in sorted(stats.keys()):
        stats_html += f"""
            <div class="stat-box">
                <span class="stat-name">{rtype}</span>
                <span class="stat-count">{stats[rtype]}</span>
            </div>"""

    # HTML principal
    html_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #333; line-height: 1.6; background-color: #fcfcfc; }}
            .container {{ max-width: 1100px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-bottom: 5px; }}
            .heure {{ color: #95a5a6; font-style: italic; margin-bottom: 20px; font-size: 0.9em; }}
            
            /* Style des Stats */
            .stats-container {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 6px; border: 1px solid #eee; }}
            .stat-box {{ background: white; border: 1px solid #ddd; border-radius: 4px; display: flex; overflow: hidden; font-size: 0.85em; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
            .stat-name {{ background: #34495e; color: white; padding: 5px 10px; font-weight: bold; }}
            .stat-count {{ padding: 5px 10px; color: #2c3e50; font-weight: bold; background: white; }}
            
            h2 {{ background: #f1f4f7; padding: 12px; border-left: 5px solid #3498db; margin-top: 40px; font-size: 1.2em; color: #2c3e50; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; border: 1px solid #e0e0e0; table-layout: fixed; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; word-wrap: break-word; }}
            th {{ background-color: #f8f9fa; color: #34495e; font-weight: bold; width: 30%; border-bottom: 2px solid #3498db; }}
            tr:hover {{ background-color: #f9fbff; }}
            code {{ background: #f0f0f0; padding: 2px 5px; border-radius: 3px; font-family: 'Consolas', monospace; color: #c7254e; font-size: 0.9em; }}
            .summary-text {{ font-size: 1.1em; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Rapport d'énumération : {target_domain}</h1>
            <div class="heure">Généré le : {heure_rapport}</div>
            
            <div class="summary-text">
                <b>Nœuds explorés :</b> {len(visited_nodes)} | <b>Total des relations :</b> {len(results)}
            </div>

            <div class="stats-container">
                {stats_html}
            </div>
    """
    # resultats par catégorie
    categories = {}
    for rtype, source, values in results:
        if rtype not in categories:
            categories[rtype] = []
        categories[rtype].append((source, values))

    for cat in categories:
        html_content += f"<h2>Section : {cat}</h2>"
        html_content += "<table><tr><th>Source</th><th>Résultats</th></tr>"
        # remplissage du tableau
        for src, vals in categories[cat]:
            if type(vals) == dict:
                val_str = ""
                for cle in vals:
                    if vals[cle]:
                        val_str += f"<b>{cle} :</b> {', '.join(vals[cle])}<br>"
            elif type(vals) == list:
                val_str = ", ".join(vals)
            else:
                val_str = str(vals)
                
            html_content += f"<tr><td><code>{src}</code></td><td>{val_str}</td></tr>"
        
        html_content += "</table>"

    # footer
    html_content += f"""
            <div style="margin-top: 50px; text-align: center; color: #bdc3c7; font-size: 0.8em; border-top: 1px solid #eee; padding-top: 20px;">
                Fin du rapport - DNS Tool  <a href="https://github.com/Uramix2/DNS-solver" style="color: #3498db; text-decoration: none; font-weight: bold;">GitHub Repository</a>
            </div>
        </div> </body>
    </html>
    """
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return filename