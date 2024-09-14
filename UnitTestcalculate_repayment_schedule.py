
import unittest
from unittest.mock import patch, Mock
from your_file import calculate_repayment_schedule  # replace 'your_file' with the actual name of your file

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_file.engine')
    def test_calculate_repayment_schedule(self, mock_engine):
        # Test connection to database
        mock_conn = mock_engine.connect.return_value
        mock_conn.execute.return_value.fetchone.return_value = (100, 10, 5, '2022-01-01')  # replace with your expected values
        loan_id = 1  # replace with your expected value
        calculate_repayment_schedule(loan_id)
        mock_engine.connect.assert_called_once()
        mock_conn.execute.assert_called_once()

    @patch('your_file.engine')
    def test_calculate_repayment_schedule_nonexistent_loan(self, mock_engine):
        # Test connection to database with non-existent loan
        mock_conn = mock_engine.connect.return_value
        mock_conn.execute.return_value.fetchone.return_value = None
        loan_id = 1  # replace with your expected value
        self.assertRaises(Exception, calculate_repayment_schedule, loan_id)
        mock_engine.connect.assert_called_once()
        mock_conn.execute.assert_called_once()

    @patch('your_file.engine')
    def test_calculate_repayment_schedule_mismatched_date_format(self, mock_engine):
        # Test connection to database with mismatched date format
        mock_conn = mock_engine.connect.return_value
        row = ('100', '10', '5', '01/01/2022')  # replace with your expected values
        mock_conn.execute.return_value.fetchone.return_value = row
        loan_id = 1  # replace with your expected value
        self.assertRaises(ValueError, calculate_repayment_schedule, loan_id)
        mock_engine.connect.assert_called_once()
        mock_conn.execute.assert_called_once()

    @patch('your_file.engine')
    def test_calculate_repayment_schedule_rounding_error(self, mock_engine):
        # Test connection to database with rounding error
        mock_conn = mock_engine.connect.return_value
        row = ('100', '10', '5', '2022-01-01')  # replace with your expected values
        mock_conn.execute.return_value.fetchone.return_value = row
        loan_id = 1  # replace with your expected value
        calculate_repayment_schedule(loan_id)
        mock_engine.connect.assert_called_once()
        mock_conn.execute.assert_called_once()

    @patch('your_file.engine')
    def test_calculate_repayment_schedule_several_calls(self, mock_engine):
        # Test connection to database with multiple calls
        mock_conn = mock_engine.connect.return_value
        row = ('100', '10', '5', '2022-01-01')  # replace with your expected values
        mock_conn.execute.return_value.fetchone.return_value = row
        loan_id = 1  # replace with your expected value
        calculate_repayment_schedule(loan_id)
        calculate_repayment_schedule(loan_id)
        calculate_repayment_schedule(loan_id)
        mock_engine.connect.assert_any_call()
        mock_conn.execute.assert_any_call()

if __name__ == '__main__':
    unittest.main()
