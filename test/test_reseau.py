
import unittest
import xmlrunner

from Reseau import Reseau
from Terrain import Terrain, Case
from contextlib import redirect_stdout
from io import StringIO

class TestReseau(unittest.TestCase):

    def test_definition_entree(self):
        # TODO
        self.fail()

    
    def test_ajout_noeud(self):
        r = Reseau()

        # Ajouter deux noeuds valides
        r.ajouter_noeud(0, (0, 1))
        r.ajouter_noeud(2, (1, 3))

        # Essayer d'ajouter un noeud avec un identifiant negatif
        r.ajouter_noeud(-1, (2, 2))

        # Essayer d'ajouter un noeud avec un identifiant existant
        r.ajouter_noeud(0, (3, 4))

        # Verifier les noeuds du reseau
        self.assertEqual(r.noeuds, {
            0: (0, 1),
            2: (1, 3)
        })


    def test_ajout_arc(self):
        r = Reseau()
        r.ajouter_noeud(0, (0, 0))
        r.ajouter_noeud(1, (1, 0))
        r.ajouter_noeud(2, (0, 1))

        r.ajouter_arc(1, 0)
        r.ajouter_arc(0, 1)
        r.ajouter_arc(0, 2)
        r.ajouter_arc(0, 3)

        self.assertEqual(r.arcs, [
            (0, 1),
            (0, 2),
        ])

    def test_validation_correcte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)
        r.arcs.append((3, 4))

        self.assertTrue(r.valider_reseau())

    def test_validation_incorrecte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)

        self.assertFalse(r.valider_reseau())

    def test_validation_sans_entree(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)

        self.assertFalse(r.valider_reseau())

    def test_distribution_correcte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)
        r.arcs.append((3, 4))

        t = Terrain()
        t.cases = [
                [Case.ENTREE, Case.VIDE, Case.VIDE],
                [Case.CLIENT, Case.VIDE, Case.CLIENT],
        ]

        self.assertTrue(r.valider_distribution(t))

    def test_distribution_incorrecte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)
        r.arcs.append((3, 4))

        t = Terrain()
        t.cases = [
                [Case.ENTREE, Case.VIDE, Case.VIDE],
                [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]

        self.assertFalse(r.valider_distribution(t))


    def test_afficher(self):
        r = Reseau()
        r.noeud_entree = 0
        r.noeuds = {0: (0, 0), 1: (1, 0)}
        r.arcs = [(0, 1)]

        output = StringIO()
        with redirect_stdout(output):
            r.afficher()

        texte = output.getvalue()
        self.assertIn("Noeud d'entrée : 0", texte)
        self.assertIn("0 : (0, 0)", texte)
        self.assertIn("0 <--> 1", texte)    

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))

