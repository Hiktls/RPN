import unittest
import asyncio
from rpn import Expression
from math import sin,tan,cos,radians


class TestParser(unittest.TestCase):
    def setUp(self):
        self.infix_to_rpn = {
        "3 + 5": ["3", "5", "+"],
        "10 + 2 * 6": ["10", "2", "6", "*", "+"],
        "( 3 + -5 ) * -2": ["3", "-5", "+", "-2", "*"],
        "5 * ( 10 + 2 )": ["5", "10", "2", "+", "*"],
        "3 + 5 * ( 2 - 8 )": ["3", "5", "2", "8", "-", "*", "+"],
        "7 + 3 * -5 / ( 10 - 5 )": ["7", "3", "-5", "*", "10", "5", "-", "/", "+"],
        "-a + b * c": ["-a", "b", "c", "*", "+"],
        "( x + y ) * z": ["x", "y", "+", "z", "*"],
        "x * ( y + z )": ["x", "y", "z", "+", "*"],
        "3 * ( 4 + 2 ) / 6": ["3", "4", "2", "+", "*", "6", "/"],
        "-5 * -9 + 3": ["-5", "-9", "*", "3", "+"],
        "sin(30)": ["30", "sin"],
        "cos(45) + 3": ["45", "cos", "3", "+"],
        "5 * tan(60)": ["5", "60", "tan", "*"],
        "sin(30) + cos(60)": ["30", "sin", "60", "cos", "+"],
        "sin(45 + 5)": ["45", "5", "+", "sin"],
        "3 * sin(90)": ["3", "90", "sin", "*"],
        "tan(45) * ( 2 + 3 )": ["45", "tan", "2", "3", "+", "*"]
    }

        self.infix_to_result = {
            "3 + 5": 8.0,
            "10 + 2 * 6": 22.0,
            "( 3 + 5 ) * 2": 16.0,
            "5 * ( 10 + 2 )": 60.0,
            "3 + 5 * ( 2 - 8 )": -27.0,
            "7 + 3 * 5 / ( 10 - 5 )": 10.0,
            "3 * ( 4 + 2 ) / 6": 3.0,
            "10 / 4": 2.5,
            "( 7 - 3 ) * ( 5 + 2 )": 28.0,
            "15 - 4 / 2": 13.0,
            "2 ^ 3": 8.0,
            "( 2 + 3 ) ^ 2": 25.0,
            "4 ^ ( 1 / 2 )": 2.0,
            "3 + 4 * 2 / ( 1 - 5 ) ^ 2": 3.5,
            "2 ^ 3 + 4 ^ 2": 24.0,
            "( 10 - 3 ) ^ ( 2 / 3 )": 3.6593,
            "6 * ( 4 + 3 ^ 2 )": 78.0,
            "( 1 + 2 ) ^ ( 3 + 1 )": 81.0,
            "100 / ( 2 ^ 3 )": 12.5,
            "sin(30)": sin((30)),
            "cos(45) + 3": cos((45)) + 3,
            "5 * tan(60)": 5 * tan((60)),
            "sin(30) + cos(60)": sin((30)) + cos((60)),
            "sin(45 + 5)": sin((45 + 5)),
            "3 * sin(90)": 3 * sin((90)),
            "tan(45) * ( 2 + 3 )": tan((45)) * 5
        }

        self.variable_test_cases = [
            ["5 * x + 3", {"x": "2"}, 13.0],
            ["5 - x / 2", {"x": "4"}, 3.0],
            ["a * b + c", {"a": "3", "b": "4", "c": "2"}, 14.0],
            ["(x + y) * z", {"x": "1", "y": "2", "z": "3"}, 9.0],
            ["m / (-n + p)", {"m": "10", "-n": "2", "p": "3"}, 10.0],
            ["x ^ 2 + 2 * x + 1", {"x": "-1"}, 0.0],
            ["a ^ b - c", {"a": "2", "b": "3", "c": "4"}, 4.0],
            ["u + v / w", {"u": "6", "v": "4", "w": "2"}, 8.0],
            ["(h - i) * (j + k)", {"h": "7", "i": "2", "j": "3", "k": "1"}, 20.0],
            ["q / -r ^ s", {"q": "16", "-r": "2", "s": "3"}, -2.0],
            ["5 * sin(x)", {"x": "30"}, 5 * sin((30))],
            ["cos(x) + y", {"x": "60", "y": "2"}, cos((60)) + 2],
            ["tan(a) * b", {"a": "45", "b": "4"}, tan((45)) * 4],
            ["sin(x + y)", {"x": "30", "y": "15"}, sin((30 + 15))],
            ["3 + sin(z) * 2", {"z": "90"}, (3 + sin(90) * 2)]
        ]

    def testParser(self):
        print("Testing Parser")
        for k,v in self.infix_to_rpn.items():
            e = Expression(k)
            self.assertEqual(e.rpn,v)
    def testEval(self):
        print("Testing Evaluations`")
        for k,v in self.infix_to_result.items():
            e = Expression(k)
            print(e.rpn)
            print(f"Evaluating {k}")
            e.alternateEval()
            self.assertAlmostEqual(e.lastEvaluation,v,4)
    def testVar(self):
        for infix in self.variable_test_cases:
            e = Expression(infix[0])
            e.variables = infix[1]
            print(f"Evaluating with variable {infix[0]}")
            e.alternateEval()
            print(e.unresolvedEval)
            self.assertAlmostEqual(e.lastEvaluation,infix[2])
        

if __name__ == "__main__":
    unittest.main()
