import unittest
from rpn import RPN



class TestParser(unittest.TestCase):
    def setUp(self):
        self.infix_to_rpn = {
            "3 + 5": ["3", "5", "+"],
            "10 + 2 * 6": ["10", "2", "6", "*", "+"],
            "( 3 + 5 ) * 2": ["3", "5", "+", "2", "*"],
            "5 * ( 10 + 2 )": ["5", "10", "2", "+", "*"],
            "3 + 5 * ( 2 - 8 )": ["3", "5", "2", "8", "-", "*", "+"],
            "7 + 3 * 5 / ( 10 - 5 )": ["7", "3", "5", "*", "10", "5", "-", "/", "+"],
            "a + b * c": ["a", "b", "c", "*", "+"],
            "( x + y ) * z": ["x", "y", "+", "z", "*"],
            "x * ( y + z )": ["x", "y", "z", "+", "*"],
            "3 * ( 4 + 2 ) / 6": ["3", "4", "2", "+", "*", "6", "/"],
            }
    
    def testParser(self):
        for k,v in self.infix_to_rpn.items():
            e = RPN(k)
            print(e)
            while "" in e.testMat:
                e.testMat.remove("")
            self.assertEqual(e.testMat,v)
        

if __name__ == "__main__":
    unittest.main()

# Write a function to print hello world