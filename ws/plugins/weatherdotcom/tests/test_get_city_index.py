import unittest
import ws.bad as bad

from ..main import weathercom_get_city_index

class get_city_indexTest(unittest.TestCase):

    def test_ahrensfelde(self):
        self.assertEqual(weathercom_get_city_index('ahrensfelde'), 'GMXX7358')

    def test_invalid_city(self):
        with self.assertRaises(bad.City):
            weathercom_get_city_index('GermanyHasManyFunCityNamesButNotThisOne')


if __name__ == '__main__':
    unittest.main()
