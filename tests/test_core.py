import unittest
from decimal import Decimal
from core import compare

class ComparisonTests(unittest.TestCase):
    def test_fictional_example(self):
        r = compare('10', '9.80', 500, 10, 125, 15)
        self.assertEqual(r['effective_a'], Decimal('9.6'))
        self.assertEqual(r['winner'], 'A')
        self.assertEqual(r['difference'], Decimal('0.20'))
        self.assertEqual(r['margin_a'], Decimal('36'))
    def test_no_benefit(self):
        self.assertEqual(compare(10, 9)['winner'], 'B')
    def test_tie(self):
        self.assertEqual(compare('0.1', '0.10')['winner'], 'Empate')
    def test_floor(self):
        self.assertEqual(compare(1, 0, 1000)['effective_a'], 0)
    def test_zero_is_quote(self):
        self.assertEqual(compare(0, 1)['winner'], 'A')
    def test_comma(self):
        self.assertEqual(compare('10,20','10,30')['difference'], Decimal('0.10'))
    def test_no_sale_margin(self):
        self.assertIsNone(compare(1,2)['margin_a'])
    def test_negative_margin(self):
        self.assertEqual(compare(10, 9, sale=5)['margin_a'], -100)
    def test_invalid(self):
        for value in ('', 'abc', '-1', 'NaN', 'Infinity', '-Infinity'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                compare(value, 1)
    def test_positive_divisors(self):
        for kwargs in ({'units':0}, {'units':-1}, {'points_per_currency':0}, {'points_per_currency':-1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                compare(1,2,**kwargs)
    def test_invalid_benefit_and_sale(self):
        for kwargs in ({'points':-1}, {'sale':'NaN'}):
            with self.assertRaises(ValueError): compare(1,2,**kwargs)

if __name__ == '__main__': unittest.main()
