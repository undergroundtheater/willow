import unittest

def IsOdd(n):
    return n % 2 == 1

class IsOddTest(unittest.TestCase):

    def testOne(self):
        self.assertEquals(IsOdd(2), False)
        self.assertEquals(IsOdd(3), True)
        pass

    def testTwo(self):
        self.assertEquals(IsOdd(2), False)
        self.assertEquals(IsOdd(4), True)
        pass

if __name__ == "__main__":
    unittest.main()