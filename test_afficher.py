
from Reseau import Reseau

# Creer un reseau
r = Reseau()

# Ajouter les noeuds
r.noeuds = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (1, 2)
}

# Definir le noeud d'entree
r.noeud_entree = 0

# Ajouter les arcs
r.arcs = [(0, 1), (1, 2), (2, 3)]

# Afficher le reseau
r.afficher()
