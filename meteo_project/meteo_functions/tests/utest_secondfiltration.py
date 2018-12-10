import unittest
from meteo_functions.second_filtration import SecondFiltration

import pandas as pd


class SecondFiltrationTest(unittest.TestCase):
    def test_filter(self):
        df_original = pd.DataFrame({
            "first_column": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "second_column": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        })
        column_name = "first_column"
        min = 2
        max = 9
        df_expected = pd.DataFrame({"first_column": [2, 3, 4, 5, 6, 7, 8, 9],
                                    "second_column": [13, 14, 15, 16, 17, 18, 19, 20]})
        df_expected.index = [2, 3, 4, 5, 6, 7, 8, 9]
        df_result = SecondFiltration.filter(df_original, column_name, min, max)
        pd.testing.assert_frame_equal(df_result, df_expected)


if __name__ == '__main__':
    unittest.main()
