import unittest
from main import Node
from main import NodeUtils


class EqualTest(unittest.TestCase):
    def testInit(self):
        a = Node([[1, 2, 3], [4, 0, 5], [6, 7, 8]], 3)
        b = Node([[1, 2, 3], [0, 4, 5], [6, 7, 8]], 4)
        assert a == a
        assert a != b
        assert Node([
            [1, 2, 3],
            [0, 4, 5],
            [6, 7, 8],
        ], 8) in [a, b]

    def test_can_move(self):
        a = Node([[1, 2, 3], [4, 0, 5], [6, 7, 8]], 3)

        assert Node.can_move(a, "L")
        assert Node.can_move(a, "U")
        assert Node.can_move(a, "D")
        assert Node.can_move(a, "R")

        a = Node([[0, 2, 3], [1, 4, 5], [6, 7, 8]], 4)
        assert not Node.can_move(a, "L")
        assert not Node.can_move(a, "U")
        assert Node.can_move(a, "D")
        assert Node.can_move(a, "R")

        a = Node([[6, 2, 3], [1, 4, 5], [0, 7, 8]], 4)
        assert not Node.can_move(a, "L")
        assert Node.can_move(a, "U")
        assert not Node.can_move(a, "D")
        assert Node.can_move(a, "R")

        a = Node([[6, 2, 3], [1, 4, 5], [8, 7, 0]], 4)
        assert Node.can_move(a, "L")
        assert Node.can_move(a, "U")
        assert not Node.can_move(a, "D")
        assert not Node.can_move(a, "R")

    def test_node_move(self):
        a = Node([[0, 2, 3], [1, 4, 5], [6, 7, 8]], 4)
        Node.move(a, "R")
        assert a == Node([[2, 0, 3], [1, 4, 5], [6, 7, 8]], 4)

        a = Node([[0, 2, 3], [1, 4, 5], [6, 7, 8]], 4)
        Node.move(a, "D")
        assert a == Node([[1, 2, 3], [0, 4, 5], [6, 7, 8]], 4)

        a = Node([[6, 2, 3], [1, 4, 5], [0, 7, 8]], 4)
        Node.move(a, "R")
        assert a == Node([[6, 2, 3], [1, 4, 5], [7, 0, 8]], 4)

        a = Node([[6, 2, 3], [1, 0, 5], [7, 4, 8]], 4)
        Node.move(a, "U")
        assert a == Node([[6, 0, 3], [1, 2, 5], [7, 4, 8]], 4)

    def test_parity(self):
        a = Node([[6, 2, 3], [1, 0, 5], [7, 4, 8]], 4)
        assert Node.get_parity(a) == False
        a = Node([[0, 2, 3], [1, 4, 5], [6, 7, 8]], 4)
        assert Node.get_parity(a) == True

    def test_heuristic_funtion(self):
        start = Node([[6, 2, 3], [1, 0, 5], [7, 4, 8]], 4)
        target = Node([[6, 3, 2], [1, 0, 5], [7, 4, 8]], 4)
        assert Node.heuristic_funtion(start, target, 1, 1) == 6
        assert Node.heuristic_funtion(target, target, 1, 1) == 4

if __name__ == '__main__':
    unittest.main()
