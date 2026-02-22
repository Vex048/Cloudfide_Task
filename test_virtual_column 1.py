
import pandas as pd
from solution import add_virtual_column
import unittest

class TestSolution(unittest.TestCase):
    def setUp(self):
        pass


    # ------------------------------------------------------------------
    # GIVEN TESTS
    # ------------------------------------------------------------------

    def test_sum_of_two_columns(self):
        df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
        df_expected = pd.DataFrame([[1, 1, 2]] * 2, columns=["label_one", "label_two", "label_three"])
        df_result = add_virtual_column(df, "label_one+label_two", "label_three")
        self.assertTrue(df_result.equals(df_expected), f"The function should sum the columns: label_one and label_two.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}")

    def test_multiplication_of_two_columns(self):
        df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
        df_expected = pd.DataFrame([[1, 1, 1]] * 2, columns=["label_one", "label_two", "label_three"])
        df_result = add_virtual_column(df, "label_one * label_two", "label_three")
        self.assertTrue(df_result.equals(df_expected), f"The function should multiply the columns: label_one and label_two.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}")

    def test_subtraction_of_two_columns(self):
        df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
        df_expected = pd.DataFrame([[1, 1, 0]] * 2, columns=["label_one", "label_two", "label_three"])
        df_result = add_virtual_column(df, "label_one - label_two", "label_three")
        self.assertTrue(df_result.equals(df_expected), f"The function should subtract the columns: label_one and label_two.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}")

    def test_empty_result_when_invalid_labels(self):
        df = pd.DataFrame([[1, 2]] * 3, columns=["label_one", "label_two"])
        df_result = add_virtual_column(df, "label_one + label_two", "label3")
        self.assertTrue(df_result.empty, f"Should return an empty df when the \"new_column\" is invalid.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df")

    def test_empty_result_when_invalid_rules(self):
        df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
        df_result = add_virtual_column(df, "label&one + label_two", "label_three")
        self.assertTrue(df_result.empty, f"Should return an empty df when the role have invalid character: '&'.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df")
        df_result = add_virtual_column(df, "label_five + label_two", "label_three")
        self.assertTrue(df_result.empty, f"Should return an empty df when the role have a column which isn't in the df: 'label_five'.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df")


    def test_when_extra_spaces_in_rules(self):
        df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
        df_expected = pd.DataFrame([[1, 1, 2]] * 2, columns=["label_one", "label_two", "label_three"])
        df_result = add_virtual_column(df, "label_one + label_two ", "label_three")
        self.assertTrue(df_result.equals(df_expected), f"Should work when the role have spaces between the operation and the column.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}")
        df_result = add_virtual_column(df, "  label_one + label_two ", "label_three")
        self.assertTrue(df_result.equals(df_expected), f"Should work when the role have extra spaces in the start/end.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}")

    # ------------------------------------------------------------------------------------
    # HANDMADE TESTS
    # ------------------------------------------------------------------------------------

    def test_invalid_new_column_name_with_numbers(self):
        df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
        df_result = add_virtual_column(df, "label_one + label_two", "new_column_1")
        self.assertTrue(df_result.empty,f"Should return an empty DF because 'new_column_1' contains a number.\nResult:\n{df_result}")

    def test_invalid_role_column_name_with_numbers(self):
        df = pd.DataFrame([[1, 1]] * 2, columns=["label_1", "label_two"])
        df_result = add_virtual_column(df, "label_1 + label_two", "label_three")
        self.assertTrue(df_result.empty,f"Should return an empty DF because 'label_1' in role contains a number.\nResult:\n{df_result}")

    def test_unsupported_mathematical_operation(self):
        df = pd.DataFrame([[4, 2]] * 2, columns=["label_one", "label_two"])
        df_result = add_virtual_column(df, "label_one / label_two", "label_three")
        self.assertTrue(df_result.empty,f"Should return an empty DF because '/' is not a supported operation.\nResult:\n{df_result}")

    def test_multiple_operations_and_precedence(self):
        df = pd.DataFrame([[2, 3, 4]] * 2, columns=["A_col", "B_col", "C_col"])
        df_expected = pd.DataFrame([[2, 3, 4, 14]] * 2, columns=["A_col", "B_col", "C_col", "result_col"])
        df_result = add_virtual_column(df, "A_col + B_col * C_col", "result_col")
        self.assertTrue(df_result.equals(df_expected),f"The function should maintain the order of mathematical operations.\nResult:\n{df_result}\nExpected:\n{df_expected}")

    def test_overwrite_existing_column(self):
        df = pd.DataFrame([[2, 3]] * 2, columns=["label_one", "label_two"])
        df_expected = pd.DataFrame([[2, 6]] * 2, columns=["label_one", "label_two"])
        df_result = add_virtual_column(df, "label_one * label_two", "label_two")
        self.assertTrue(df_result.equals(df_expected),f"The function should allow overwriting an existing column.\nResult:\n{df_result}\nExpected:\n{df_expected}")

    def test_tabs_and_newlines_in_role(self):
        df = pd.DataFrame([[5, 3]] * 2, columns=["label_one", "label_two"])
        df_expected = pd.DataFrame([[5, 3, 2]] * 2, columns=["label_one", "label_two", "label_three"])
        df_result = add_virtual_column(df, "label_one\t-\nlabel_two", "label_three")
        self.assertTrue(df_result.equals(df_expected),f"Should ignore tabs and newline characters in role.\nResult:\n{df_result}")

if __name__ == "__main__":
    unittest.main()
