from unittest import TestCase

from gridding import KILOMETER, METER, FR, GPS, Grid, Resolution


class TestGrid(TestCase):
    grid = Grid(Resolution(200, METER))

    def test_from_address(self):
        code, tile = self.grid.from_address(
            " 9, boulevard Gouvion Saint-Cyr - 75017 Paris",
            FR(filepath="../../data/fr_address_repository_test.csv"),
        )
        self.assertEqual(code, "WGS84|RES200m|N4888413|E0228839")
        self.assertEqual(tile.to_string(), "4207.2719")

    def test_from_gps(self):
        code, tile = self.grid.from_gps(GPS(2, 45))
        self.assertEqual(code, "WGS84|RES200m|N4499998|E0199812")
        self.assertEqual(tile.to_string(), "2048.2809")
        close_point, _ = self.grid.from_gps(GPS(2.0005, 45.0005))
        self.assertEqual(code, close_point)
        off_grid, off_tile = self.grid.from_gps(GPS(-10, -6))
        self.assertEqual(off_grid, "WGS84|RES200m|S0599990|W0999938")
        self.assertEqual(off_tile.to_string(), "-26196.-2673")


class TestResolution(TestCase):
    def test_to_string(self):
        res = Resolution(200, METER)
        self.assertEqual(res.to_string(), "RES200m")
        res = Resolution(1, KILOMETER)
        self.assertEqual(res.to_string(), "RES1km")
        with self.assertRaises(Exception):
            Resolution(56, "dl")
