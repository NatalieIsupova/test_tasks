import unittest
from meteo_functions.grouping import Group
import pandas as pd


class GroupTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        print("==========")
        print("tearDownClass")

    def test_make(self):
        df_original = pd.DataFrame({"first_column": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                    "second_column": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]})
        column_name = "first_column"
        min = 2
        max = 9
        step = 3
        df_expected = [
            (3.5, pd.DataFrame({'first_column': [2, 3, 4], 'second_column': [13, 14, 15]}, index=[2, 3, 4])),
            (6.5, pd.DataFrame({'first_column': [5, 6, 7], 'second_column': [16, 17, 18]}, index=[5, 6, 7])),
            (9.5, pd.DataFrame({'first_column': [8, 9, 10], 'second_column': [19, 20, 21]}, index=[8, 9, 10]))]

        df_result = Group.make(df_original, column_name, min, max, step)
        for i, tuple_group in enumerate(df_result):
            group_name, df = tuple_group
            self.assertEqual(group_name, df_expected[i][0])
            pd.testing.assert_frame_equal(df, df_expected[i][1])


if __name__ == '__main__':
    unittest.main()
