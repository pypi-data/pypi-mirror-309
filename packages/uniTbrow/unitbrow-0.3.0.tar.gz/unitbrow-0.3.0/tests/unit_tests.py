import unittest
import uniTbrow as ub


class UnitTests(unittest.TestCase):
    def test_unit_equality(self):
        self.assertEqual(ub.units.metre, ub.units.metre)


if __name__ == '__main__':
    unittest.main()
