import unittest

from add.add_by_three import add_by_three


class TestDivideByThree(unittest.TestCase):

    def test_add_by_three(self):
        self.assertEqual(add_by_three(12), 4)

unittest.main()