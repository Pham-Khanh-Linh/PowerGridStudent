
from Terrain import Terrain, Case
from StrategieReseau import StrategieReseau, StrategieReseauAuto

class Reseau:
    def __init__(self):
        self.strat = StrategieReseauAuto()
        self.noeuds = {}
        self.arcs = []

        self.noeud_entree = -1

    def definir_entree(self, n: int) -> None:
        if n in self.noeuds.keys():
            self.noeud_entree = n
        else:
            self.noeud_entree = -1

    def ajouter_noeud(self, n: int, coords: tuple[int, int]):
        if n >= 0 and n not in self.noeuds:
            self.noeuds[n] = coords

    def ajouter_arc(self, n1: int, n2: int) -> None:
        if n1 > n2:
            tmp = n2
            n2 = n1
            n1 = tmp
        if n1 not in self.noeuds.keys() or n2 not in self.noeuds.keys():
            return
        if (n1, n2) not in self.arcs:
            self.arcs.append((n1, n2))

    def set_strategie(self, strat: StrategieReseau):
        self.strat = strat

    def valider_reseau(self) -> bool:
        #Vérifier le noeud d'entrée et les noeuds
        # Le reseau n'est pas null et le noeud d'entrée est bien dans les noeuds
        if not self.noeuds or self.noeud_entree not in self.noeuds:
            return False

        #Construire un dictionnaire de voisins pour chaque noeud 
        # Exemple: si on a arcs = [(0, 1), (1, 2), (2, 3)] donc
        #  voisins = {0: {1}, 1: {0, 2}, 2: {1, 3}, 3: {2}}
        voisins = {n: set() for n in self.noeuds}
        
        for n1, n2 in self.arcs:
            if n1 not in voisins and n2 not in voisins:
                return False
            voisins[n1].add(n2)
            voisins[n2].add(n1)

        # Parcours en profondeur depuis le noeud d'entree
        visites = {self.noeud_entree}
        a_visiter = [self.noeud_entree]
        while a_visiter:
            noeud = a_visiter.pop()
            for voisin in voisins[noeud] - visites:
                visites.add(voisin)
                a_visiter.append(voisin)

        # Verifier que tous les noeuds sont connectes
        return len(visites) == len(self.noeuds)

    def valider_distribution(self, t: Terrain) -> bool:
        if not self.valider_reseau():
            return False

        if self.noeuds[self.noeud_entree] != t.get_entree():
            return False

        # Verifier que tous les clients sont couverts
        noeuds_reseau = set(self.noeuds.values())
        for client in t.get_clients():
            if client not in noeuds_reseau:
                return False
        return True

    def configurer(self, t: Terrain):
        self.noeud_entree, self.noeuds, self.arcs  = self.strat.configurer(t)

    def afficher(self) -> None:
        print("=== Reseau electrique ===")

        # Afficher le noeud d'entree
        print(f"Noeud d'entrée : {self.noeud_entree}")

        # Afficher les noeuds du reseau
        print("Noeuds :")
        if self.noeuds:
            for identifiant, coords in sorted(self.noeuds.items()):
                print(f"  {identifiant} : {coords}")
        else:
            print("  (aucun)")

        # Afficher les arcs du reseau
        print("Arcs :")
        if self.arcs:
            for n1, n2 in sorted(self.arcs):
                print(f"  {n1} <--> {n2}")
        else:
            print("  (aucun)")

    def afficher_avec_terrain(self, t: Terrain) -> None:
        for ligne, l in enumerate(t.cases):
            for colonne, c in enumerate(l):
                if (ligne, colonne) not in self.noeuds.values():
                    if c == Case.OBSTACLE:
                        print("X", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("~", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
                else:
                    if c == Case.OBSTACLE:
                        print("T", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("+", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
            print()

    def calculer_cout(self, t: Terrain) -> float:
        cout = 0
        for _ in self.arcs:
            cout += 1.5
        for n in self.noeuds.values():
            if t[n[0]][n[1]] == Case.OBSTACLE:
                cout += 2
            else:
                cout += 1
        return cout

