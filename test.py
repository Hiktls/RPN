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

        self.infix_to_result = {
           "3 + 5": 8.0,
            "10 + 2 * 6": 22.0,
            "( 3 + 5 ) * 2": 16.0,
            "5 * ( 10 + 2 )": 60.0,
            "3 + 5 * ( 2 - 8 )": -27.0,  # Fixed
            "7 + 3 * 5 / ( 10 - 5 )": 10.0,
            "3 * ( 4 + 2 ) / 6": 3.0,
            "10 / 4": 2.5,
            "( 7 - 3 ) * ( 5 + 2 )": 28.0,
            "15 - 4 / 2": 13.0,
            "2 ^ 3": 8.0,
            "( 2 + 3 ) ^ 2": 25.0,
            "4 ^ ( 1 / 2 )": 2.0,  # Square root
            "3 + 4 * 2 / ( 1 - 5 ) ^ 2": 3.5,
            "2 ^ 3 + 4 ^ 2": 24.0,
            "( 10 - 3 ) ^ ( 2 / 3 )": 3.6593,  # Fixed approximation
            "6 * ( 4 + 3 ^ 2 )": 78.0,  # Fixed
            "( 1 + 2 ) ^ ( 3 + 1 )": 81.0,
            "100 / ( 2 ^ 3 )": 12.5,
        }

        self.variable_test_cases = [
            ["5 * x + 3", {"x": "2"}, 13.0],  # 5 * 2 + 3 = 13
            ["5 - x / 2", {"x": "4"}, 3.0],  # 5 - 4 / 2 = 3
            ["a * b + c", {"a": "3", "b": "4", "c": "2"}, 14.0],  # 3 * 4 + 2 = 14
            ["(x + y) * z", {"x": "1", "y": "2", "z": "3"}, 9.0],  # (1 + 2) * 3 = 9
            ["m / (n + p)", {"m": "10", "n": "2", "p": "3"}, 2.0],  # 10 / (2 + 3) = 2
            ["x ^ 2 + 2 * x + 1", {"x": "-1"}, 0.0],  # (-1)^2 + 2*(-1) + 1 = 0
            ["a ^ b - c", {"a": "2", "b": "3", "c": "4"}, 4.0],  # 2^3 - 4 = 4
            ["u + v / w", {"u": "6", "v": "4", "w": "2"}, 8.0],  # 6 + 4 / 2 = 8
            ["(h - i) * (j + k)", {"h": "7", "i": "2", "j": "3", "k": "1"}, 20.0],  # (7 - 2) * (3 + 1) = 20
            ["q / r ^ s", {"q": "16", "r": "2", "s": "3"}, 2.0],  # 16 / (2^3) = 2
        ]
    def testParser(self):
        print("Testing Parser")
        for k,v in self.infix_to_rpn.items():
            e = RPN(k)
            print(e)
            self.assertEqual(e.testMat,v)
    def testEval(self):
        print("Testing Evaluations`")
        for k,v in self.infix_to_result.items():
            e = RPN(k)
            print(f"Evaluating {k}")
            print(e.testMat)
            e.alternateEval()
            self.assertAlmostEqual(e.lastEvaluation,v,4)
    def testVar(self):
        for infix in self.variable_test_cases:
            e = RPN(infix[0])
            e.variables = infix[1]
            e.alternateEval()
            print(f"Evaluating {infix[0]}")
            self.assertAlmostEqual(e.lastEvaluation,infix[2])
        

if __name__ == "__main__":
    unittest.main()

# Write a function to print hello world