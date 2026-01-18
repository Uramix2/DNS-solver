from scan import *



def scan_all(domain,depth_max,current_depth=0,visited=None):
    """
    Utilise les fonctions pour scanner les différents enregistrment dns de manière récursive jusqu'à une profondeur max 
    en faisant par chaque information 
    """
    if visited is None:
        visited = set()
    
    if current_depth > depth_max:
        return []
    
    scans = []

    for e in [scan_a, scan_aaaa, scan_mx, scan_cname, scan_ns, scan_txt, scan_srv, scan_ptr]:
        result = e(domain)

        if result:
            scans.append((result, e.__name__))

            for r in result:
                if r not in visited:
                    visited.add(r)
                    scans.extend(scan_all(r, depth_max, current_depth + 1, visited))
    return scans



if __name__ == "__main__":
    # -- test --
    print(scan_all("oteria.fr",9))
                

          
        

