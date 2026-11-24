
from Terrain import Terrain, Case
from heapq import heappop, heappush

class StrategieReseau:
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        return -1, {}, []

class StrategieReseauManuelle(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        position_entree = t.get_entree()
        if position_entree == (-1, -1):
            print("Impossible de configurer le réseau : le terrain ne contient pas d'entrée.")
            return -1, {}, []

        noeuds = {0: position_entree}
        identifiants = {position_entree: 0}

        print("Configuration manuelle du réseau")
        print(f"Nœud d'entrée 0 : {position_entree}")
        print("Ajoutez les coordonnées des autres nœuds sous la forme « ligne colonne ».")
        print("Appuyez sur Entrée sans saisir de coordonnées pour terminer.")

        while True:
            saisie = input("Coordonnées du nœud : ").strip()
            if not saisie:
                break

            coordonnees = saisie.split()
            if len(coordonnees) != 2:
                print("Saisie invalide : indiquez une ligne et une colonne.")
                continue
            try:
                ligne, colonne = map(int, coordonnees)
            except ValueError:
                print("Saisie invalide : la ligne et la colonne doivent être des entiers.")
                continue

            if not (0 <= ligne < len(t.cases) and 0 <= colonne < len(t.cases[ligne])):
                print("Saisie invalide : ces coordonnées sont hors du terrain.")
                continue

            position = (ligne, colonne)
            if position in identifiants:
                print(f"Cette case est déjà le nœud {identifiants[position]}.")
                continue

            identifiant = len(noeuds)
            noeuds[identifiant] = position
            identifiants[position] = identifiant

        print("Nœuds disponibles :")
        for identifiant, position in noeuds.items():
            print(f"  {identifiant} : {position}")

        print("Ajoutez les liaisons sous la forme « identifiant1 identifiant2 ».")
        print("Appuyez sur Entrée sans saisir de liaison pour terminer.")

        arcs = []
        arcs_existants = set()
        while True:
            saisie = input("Liaison : ").strip()
            if not saisie:
                break

            extremites = saisie.split()
            if len(extremites) != 2:
                print("Saisie invalide : indiquez deux identifiants de nœuds.")
                continue
            try:
                n1, n2 = map(int, extremites)
            except ValueError:
                print("Saisie invalide : les identifiants doivent être des entiers.")
                continue

            if n1 not in noeuds or n2 not in noeuds or n1 == n2:
                print("Saisie invalide : les deux identifiants doivent désigner des nœuds distincts.")
                continue

            position1, position2 = noeuds[n1], noeuds[n2]
            if abs(position1[0] - position2[0]) + abs(position1[1] - position2[1]) != 1:
                print("Saisie invalide : les nœuds reliés doivent être voisins.")
                continue

            arc = tuple(sorted((n1, n2)))
            if arc not in arcs_existants:
                arcs.append(arc)
                arcs_existants.add(arc)

        return 0, noeuds, arcs

class StrategieReseauAuto(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        position_entree = t.get_entree()
        if position_entree == (-1, -1):
            return -1, {}, []

        noeuds = {0: position_entree}
        identifiants = {position_entree: 0}
        arcs = []
        arcs_existants = set()
        connectes = {position_entree}

        for client in t.get_clients():
            if client in connectes:
                continue

            distances = {position: 0 for position in connectes}
            precedents = {}
            a_visiter = [(0, position) for position in connectes]

            while a_visiter:
                distance, position = heappop(a_visiter)
                if distance != distances[position]:
                    continue
                if position == client:
                    break

                ligne, colonne = position
                for voisin in (
                    (ligne - 1, colonne),
                    (ligne + 1, colonne),
                    (ligne, colonne - 1),
                    (ligne, colonne + 1),
                ):
                    l, c = voisin
                    if not (0 <= l < len(t.cases) and 0 <= c < len(t.cases[l])):
                        continue

                    cout_case = 2 if t.cases[l][c] == Case.OBSTACLE else 1
                    nouvelle_distance = distance + 1.5 + cout_case
                    if nouvelle_distance < distances.get(voisin, float("inf")):
                        distances[voisin] = nouvelle_distance
                        precedents[voisin] = position
                        heappush(a_visiter, (nouvelle_distance, voisin))

            if client not in distances:
                return -1, {}, []

            chemin = [client]
            while chemin[-1] not in connectes:
                chemin.append(precedents[chemin[-1]])
            chemin.reverse()

            for position in chemin:
                if position not in identifiants:
                    identifiant = len(noeuds)
                    noeuds[identifiant] = position
                    identifiants[position] = identifiant
                connectes.add(position)

            for position1, position2 in zip(chemin, chemin[1:]):
                arc = tuple(sorted((identifiants[position1], identifiants[position2])))
                if arc not in arcs_existants:
                    arcs.append(arc)
                    arcs_existants.add(arc)

        return 0, noeuds, arcs

