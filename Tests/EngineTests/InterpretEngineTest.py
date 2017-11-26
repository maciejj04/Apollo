import unittest
import numpy as np
from src.Engine.InterpretEngine import InterpretEngine


class InterpretEngineTest(unittest.TestCase):
    def testshouldReturnProperCrossCorr(self):
        a = np.array([1, 3, -2, 4])
        b = np.array([2, 3, -1, 3])
    
        ie = InterpretEngine("mockA", "mockB")
        corrValue = ie.measureNormalizedCrossCorelation(a, b)
        self.assertEqual(corrValue, 0.95173373453360122)  # :'D


if __name__ == '__main__':
    unittest.main()

