
import unittest
from datetime import datetime
from my_module import my_function  # Assuming the function is in my_module.py

class TestMyFunction(unittest.TestCase):

    def test_my_function正常使用(self):
        date_start = datetime(2021, 1, 1)
        date_end = datetime(2021, 12, 31)
        result = my_function(date_start, date_end)
        self.assertIsInstance(result, pd.DataFrame)

    def test_my_function_date_start_larger_than_date_end(self):
        date_start = datetime(2021, 12, 31)
        date_end = datetime(2021, 1, 1)
        with self.assertRaises(ValueError):
            my_function(date_start, date_end)

    def test_my_function_date_start_invalid(self):
        date_start = '2021-01-01'
        date_end = datetime(2021, 12, 31)
        with self.assertRaises(TypeError):
            my_function(date_start, date_end)

    def test_my_function_date_end_invalid(self):
        date_start = datetime(2021, 1, 1)
        date_end = '2021-12-31'
        with self.assertRaises(TypeError):
            my_function(date_start, date_end)

    def test_my_function_no_data_found(self):
        date_start = datetime(2020, 1, 1)
        date_end = datetime(2020, 1, 1)
        result = my_function(date_start, date_end)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
