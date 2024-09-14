
import unittest
from unittest.mock import patch
from your_module import calculate_repayment_schedule  # Replace with the actual module name

class TestCalculateRepaymentSchedule(unittest.TestCase):
    @patch('your_module.engine')
    @patch('pandas.read_sql_query')
    @patch('pandas.Timedelta')
    def test_calculate_repayment_schedule(self, td_mock, pq_mock, engine_mock):
        # Test valid input
        loan_id = 123
        loan_data = pd.DataFrame({'loanamount': [10000], 'interestrate': [5], 'loanterm': [5], 'startdate': ['2022-01-01']})
        pq_mock.return_value = loan_data
        td_mock.return_value = pd.Timedelta(days=30)
        engine_mock.connect.return_value = {'execute': lambda x: None, 'close': lambda: None}
        calculate_repayment_schedule(loan_id)
        
        # Verify repayment schedule was created
        # Replace this with actual assertions, e.g.:
        self.assertTrue(os.path.exists('repayment_schedule.sql'))
        
        # Test invalid input (non-integer loan ID)
        loan_id = 'abc'
        with self.assertRaises(Exception):
            calculate_repayment_schedule(loan_id)
        
        # Test invalid input (loan ID not found)
        loan_id = 9999
        pq_mock.return_value = None
        with self.assertRaises(Exception):
            calculate_repayment_schedule(loan_id)
        
        # Test invalid input (invalid interest rate)
        loan_id = 123
        loan_data = pd.DataFrame({'loanamount': [10000], 'interestrate': ['abc'], 'loanterm': [5], 'startdate': ['2022-01-01']})
        pq_mock.return_value = loan_data
        with self.assertRaises(Exception):
            calculate_repayment_schedule(loan_id)
        
        # Test invalid input (invalid loan term)
        loan_id = 123
        loan_data = pd.DataFrame({'loanamount': [10000], 'interestrate': [5], 'loanterm': 'abc', 'startdate': ['2022-01-01']})
        pq_mock.return_value = loan_data
        with self.assertRaises(Exception):
            calculate_repayment_schedule(loan_id)
        
        # Test invalid input (start date is not a date)
        loan_id = 123
        loan_data = pd.DataFrame({'loanamount': [10000], 'interestrate': [5], 'loanterm': [5], 'startdate': ['abc']})
        pq_mock.return_value = loan_data
        with self.assertRaises(Exception):
            calculate_repayment_schedule(loan_id)
        
if __name__ == '__main__':
    unittest.main()
