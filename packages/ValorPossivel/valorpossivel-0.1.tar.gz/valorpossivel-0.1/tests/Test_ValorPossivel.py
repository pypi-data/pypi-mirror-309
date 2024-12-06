# tests/test_Valor_Possivel.py

import unittest
from ValorPossivel import valorpossivel


class Test_ValorPossivel(unittest.TestCase):

    def testvalorpossivel(self):
        lista1 = [1,2,3,4,5,6]
        lista2 = [2,4,6,8]
        lista3 = ['An','Ana','Anal','Anali']

        self.assertAlmostEqual(valorpossivel(lista1), lista1)
        self.assertAlmostEqual(valorpossivel(lista2), lista2)
        self.assertAlmostEqual(valorpossivel(lista3), lista3)

if __name__ == '__main__':
    unittest.main()

