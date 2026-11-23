
import unittest
import xmlrunner
import os
import tempfile
from Terrain import Terrain, Case

class TestTerrain(unittest.TestCase):

    def test_chargement(self):
        # Test du terrain t1
        t = Terrain()
        t.charger("terrains/t1.txt")

        self.assertEqual(t.largeur, 21)
        self.assertEqual(t.hauteur, 10)
        self.assertEqual(t.get_entree(), (9, 17))
        self.assertEqual(len(t.get_clients()), 3)

        self.assertEqual(t[0][0], Case.VIDE)
        self.assertEqual(t[2][2], Case.OBSTACLE)
        self.assertEqual(t[2][10], Case.CLIENT)
        self.assertEqual(t[9][17], Case.ENTREE)

        # Test du terrain t2
        t.charger("terrains/t2.txt")

        self.assertEqual(t.largeur, 21)
        self.assertEqual(t.hauteur, 10)
        self.assertEqual(t.get_entree(), (5, 4))
        self.assertEqual(len(t.get_clients()), 7)

        self.assertEqual(t[0][0], Case.VIDE)
        self.assertEqual(t[0][12], Case.OBSTACLE)
        self.assertEqual(t[1][3], Case.CLIENT)
        self.assertEqual(t[5][4], Case.ENTREE)



    def test_get_entree(self):
        t = Terrain()
        t.cases = [
                [Case.VIDE, Case.VIDE, Case.ENTREE],
                [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]
        entree = t.get_entree()
        self.assertIsNotNone(entree)
        self.assertEqual(entree[0], 0)
        self.assertEqual(entree[1], 2)

    def test_accesseur(self):
        t = Terrain()
        t.cases = [
                [Case.ENTREE, Case.VIDE, Case.VIDE],
                [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]
        self.assertEqual(t[0][0], Case.ENTREE)
        self.assertEqual(t[0][1], Case.VIDE)
        self.assertEqual(t[1][2], Case.CLIENT)

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))

