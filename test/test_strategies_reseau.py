
import unittest
import xmlrunner
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from Terrain import Terrain, Case
from Reseau import Reseau
from StrategieReseau import StrategieReseauAuto, StrategieReseauManuelle

class TestStrategiesReseau(unittest.TestCase):

    def test_config_auto(self):
        r = Reseau()
        r.set_strategie(StrategieReseauAuto())

        t = Terrain()
        t.charger("terrains/t1.txt")
        r.configurer(t)

        self.assertTrue(r.valider_reseau())
        self.assertTrue(r.valider_distribution(t))

        t.charger("terrains/t2.txt")
        r.configurer(t)

        self.assertTrue(r.valider_reseau())
        self.assertTrue(r.valider_distribution(t))

    def test_config_auto_sans_entree(self):
        t = Terrain()
        t.cases = [[Case.CLIENT]]

        self.assertEqual(StrategieReseauAuto().configurer(t), (-1, {}, []))

    def test_config_manuel(self):
        r = Reseau()
        r.set_strategie(StrategieReseauManuelle())

        t = Terrain()
        t.cases = [[
            Case.ENTREE,
            Case.CLIENT,
            Case.VIDE,
        ]]

        saisies = ["0 1", "0 2", "", "0 1", "1 2", ""]
        with patch("builtins.input", side_effect=saisies), redirect_stdout(StringIO()):
            r.configurer(t)

        self.assertEqual(r.noeud_entree, 0)
        self.assertEqual(r.noeuds, {0: (0, 0), 1: (0, 1), 2: (0, 2)})
        self.assertEqual(r.arcs, [(0, 1), (1, 2)])
        self.assertTrue(r.valider_distribution(t))

    def test_config_manuel_sans_entree(self):
        t = Terrain()
        t.cases = [[]]

        with redirect_stdout(StringIO()):
            resultat = StrategieReseauManuelle().configurer(t)

        self.assertEqual(resultat, (-1, {}, []))

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))

