import os
import sys
import unittest
from unittest import TestCase

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../precise_rounding')))

from precise_rounding import precise_rounding


class Test(TestCase):

    def test_01(self):
        """oczywiste użycie, domyślna ilość cyfr"""
        supplied = 123.456789, 0.01269
        expected = '123.457', '0.013'
        result = precise_rounding(*supplied)
        self.assertEqual(expected, result)

    def test_02(self):
        """oczywiste użycie, trzy parametry"""
        supplied = 123.456789, 0.01269, 3
        expected = '123.4568', '0.0127'
        result = precise_rounding(*supplied)
        self.assertEqual(expected, result)

    def test_03(self):
        """zerowa niepewność, dwa parametry"""
        supplied = 123.456789, 0
        expected = '123.456789', '0'
        result = precise_rounding(*supplied)
        self.assertEqual(expected, result)

    def test_04(self):
        """zerowa niepewność, trzy parametry"""
        supplied = 123.456789, 0, 4
        expected = '123.456789', '0'
        result = precise_rounding(*supplied)
        self.assertEqual(expected, result)

    def test_05(self):
        """zaokrąglanie wartości"""
        cases = (((123.001, 0.1), ('123.00', '0.10')),
                 ((123.002, 0.1), ('123.00', '0.10')),
                 ((123.003, 0.1), ('123.00', '0.10')),
                 ((123.004, 0.1), ('123.00', '0.10')),
                 ((123.005, 0.1), ('123.01', '0.10')),
                 ((123.006, 0.1), ('123.01', '0.10')),
                 ((123.007, 0.1), ('123.01', '0.10')),
                 ((123.008, 0.1), ('123.01', '0.10')),
                 ((123.009, 0.1), ('123.01', '0.10')),
                 ((-123.002, 0.1), ('-123.00', '0.10')),
                 ((-123.001, 0.1), ('-123.00', '0.10')),
                 ((-123.003, 0.1), ('-123.00', '0.10')),
                 ((-123.004, 0.1), ('-123.00', '0.10')),
                 ((-123.005, 0.1), ('-123.01', '0.10')),
                 ((-123.006, 0.1), ('-123.01', '0.10')),
                 ((-123.007, 0.1), ('-123.01', '0.10')),
                 ((-123.008, 0.1), ('-123.01', '0.10')),
                 ((-123.009, 0.1), ('-123.01', '0.10')),)

        for supplied, expected in cases:
            with self.subTest(supplied=supplied):
                result = precise_rounding(*supplied)
                self.assertEqual(expected, result)

    def test_exceptions(self):
        """testowanie wyjątków"""

        cases = ((('abc', 0.01), TypeError), ((10.0, 'abc'), TypeError),
                 ((1.0, 0.01, 'abc'), TypeError), ((1.0, -0.01), ValueError),
                 ((1.0, 0.01, 0), ValueError), ((1.0, 0.01, -1), ValueError))

        for parameters, exception in cases:
            with self.subTest(parameters=parameters):
                with self.assertRaises(exception):
                    precise_rounding(*parameters)


if __name__ == '__main__':
    unittest.main()
