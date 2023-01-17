import unittest
from polynomials import *


class Test(unittest.TestCase):
    def setUp(self):
        self.polynomial = Polynomial()
        self.polynomial2 = Polynomial()

    def test_string(self):
        self.polynomial.insert_node(Node(1, 2))
        self.polynomial.insert_node(Node(5.2, 6))
        self.polynomial.insert_node(Node(2, 6))
        self.polynomial.insert_node(Node(3, 0))
        self.polynomial.insert_node(Node(-3, 3))

        self.assertTrue(str(self.polynomial) == "7.2x^6 + (-3x^3) + 1x^2 + 3")

        self.polynomial.insert_node(Node(0, 4))
        self.polynomial.insert_node(Node(2.5, 10))

        self.assertTrue(str(self.polynomial) == "2.5x^10 + 7.2x^6 + (-3x^3) + 1x^2 + 3")

    def test_equality(self):
        self.polynomial.insert_node(Node(5, 1.2))
        self.polynomial.insert_node(Node(3, 0))
        self.polynomial.insert_node(Node(9, 1))
        self.polynomial.insert_node(Node(2, 5))

        self.polynomial2.insert_node(Node(2.0, 5))
        self.polynomial2.insert_node(Node(9, 1))
        self.polynomial2.insert_node(Node(5, 1.2))
        self.polynomial2.insert_node(Node(3, 0))

        self.assertTrue(self.polynomial == self.polynomial2)

        self.polynomial2.insert_node(Node(10, 1))
        self.assertTrue(self.polynomial != self.polynomial2)

    def test_size(self):
        self.assertTrue(self.polynomial.size() == 0)
        self.polynomial.insert_node(Node(8, 1))
        self.polynomial.insert_node(Node(4, 5))
        self.assertTrue(self.polynomial.size() == 2)
        self.polynomial.delete_node(Node(4, 5))
        self.assertTrue(self.polynomial.size() == 1)

    def test_polynomial_degree(self):
        self.polynomial.insert_node(Node(3, 6))
        self.polynomial.insert_node(Node(3, 8))
        self.polynomial.insert_node(Node(9, 4))
        self.polynomial.insert_node(Node(2, 10))
        self.assertTrue(self.polynomial.polynomial_degree() == 10)

    def test_horner(self):
        self.polynomial.insert_node(Node(1, 3))
        self.polynomial.insert_node(Node(1, 0))
        self.assertTrue(self.polynomial.horner(2) == 9)
        self.polynomial.insert_node(Node(-6, 2))
        self.polynomial.insert_node(Node(1, 2))
        self.assertTrue(self.polynomial.horner(1) == -3)

    def test_add(self):
        self.polynomial.insert_node(Node(1.3, 2))
        self.polynomial.insert_node(Node(2, 4))
        self.polynomial.insert_node(Node(-5, 0))
        self.polynomial.insert_node(Node(4, 2))

        self.polynomial2.insert_node(Node(3, 0))
        self.polynomial2.insert_node(Node(4, 0))
        self.polynomial2.insert_node(Node(-8, 1))
        self.polynomial2.insert_node(Node(2, 2))
        self.polynomial2.insert_node(Node(1.75, 3))

        self.assertTrue(str(self.polynomial + self.polynomial2) == "2x^4 + 1.75x^3 + 7.3x^2 + (-8x^1) + 2")
        self.polynomial.insert_node(Node(-3, 0))
        self.polynomial.insert_node(Node(-4, 0))

        self.polynomial2.insert_node(Node(-2, 4))

        self.assertTrue(str(self.polynomial + self.polynomial2) == "1.75x^3 + 7.3x^2 + (-8x^1) + (-5)")

    def test_subtract(self):
        self.polynomial.insert_node(Node(1, 2))
        self.polynomial.insert_node(Node(2.2, 4))
        self.polynomial.insert_node(Node(-5, 0))
        self.polynomial.insert_node(Node(4, 2))

        self.polynomial2.insert_node(Node(3, 0))
        self.polynomial2.insert_node(Node(4, 0))
        self.polynomial2.insert_node(Node(-8, 1))
        self.polynomial2.insert_node(Node(2.18, 2))
        self.polynomial2.insert_node(Node(1, 3))

        self.assertTrue(str(self.polynomial - self.polynomial2) == "2.2x^4 + (-1x^3) + 2.82x^2 + 8x^1 + (-12)")
        self.assertTrue(str(self.polynomial2 - self.polynomial) == "(-2.2x^4) + 1x^3 + (-2.82x^2) + (-8x^1) + 12")

    def test_multiplicate(self):
        self.polynomial.insert_node(Node(1, 2))
        self.polynomial.insert_node(Node(2, 4))
        self.polynomial.insert_node(Node(-5, 0))
        self.polynomial.insert_node(Node(4, 2))

        self.polynomial2.insert_node(Node(3, 0))
        self.polynomial2.insert_node(Node(4, 0))
        self.polynomial2.insert_node(Node(-8, 1))
        self.polynomial2.insert_node(Node(2.9, 2))
        self.polynomial2.insert_node(Node(1, 3))

        self.assertTrue(
            str(self.polynomial * self.polynomial2) == "2x^7 + 5.8x^6 + (-11x^5) + 28.5x^4 + (-45x^3) + 20.5x^2 + 40x^1 + (-35)")

        self.polynomial.insert_node(Node(2, 1))
        self.polynomial2.insert_node(Node(-2, 1))

        self.assertTrue(
            str(self.polynomial * self.polynomial2) == "2x^7 + 5.8x^6 + (-15x^5) + 30.5x^4 + (-49.2x^3) + 0.5x^2 + 64x^1 + (-35)")

    def test_divide(self):
        self.polynomial.insert_node(Node(1, 2))
        self.polynomial.insert_node(Node(2.8, 4))
        self.polynomial.insert_node(Node(-5, 0))
        self.polynomial.insert_node(Node(4, 2))

        self.polynomial2.insert_node(Node(3, 0))
        self.polynomial2.insert_node(Node(4, 0))
        self.polynomial2.insert_node(Node(-8, 1))
        self.polynomial2.insert_node(Node(2.1, 2))
        self.polynomial2.insert_node(Node(1, 3))

        quotient, remainder = divmod(self.polynomial, self.polynomial2)
        self.assertTrue(str(quotient) == "2.8x^1 + (-5.88)")
        self.assertTrue(str(remainder) == "39.748x^2 + (-66.64x^1) + 36.16")

        self.polynomial2.insert_node(Node(3, 8))
        with self.assertRaises(ValueError):
            divmod(self.polynomial, self.polynomial2)

        self.polynomial.insert_node(Node(1, 5))
        self.polynomial.insert_node(Node(1, 1))

        quotient, remainder = divmod(self.polynomial2, self.polynomial)
        self.assertTrue(str(quotient) == "3.0x^3 + (-8.4x^2) + 23.52x^1 + (-80.856)")
        self.assertTrue(str(remainder) == "265.3968x^4 + (-93.2x^3) + 340.86x^2 + 190.456x^1 + (-397.28)")


if __name__ == "__main__":
    unittest.main()
