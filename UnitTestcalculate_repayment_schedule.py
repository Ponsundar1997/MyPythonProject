
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_valid_loan(self, mock_engine):
        mock_engine.connect().execute.return_value = [(10000, 5, 36, '2020-01-01')]

        loan_id = 1
        repayment_schedule = calculate_repayment_schedule(loan_id)
        self.assertEqual(len(repayment_schedule), 36)

        # check that each element in repayment_schedule is a dictionary
        for payment in repayment_schedule:
            self.assertIsInstance(payment, dict)

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_invalid_loan_id(self, mock_engine):
        mock_engine.connect().execute.return_value = None

        loan_id = 1
        with self.assertRaises(RuntimeError):
            calculate_repayment_schedule(loan_id)

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_invalid_query(self, mock_engine):
        mock_engine.connect().execute.side_effect = SQLAlchemyError()

        loan_id = 1
        with self.assertRaises(SQLAlchemyError):
            calculate_repayment_schedule(loan_id)

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_empty_result(self, mock_engine):
        mock_engine.connect().execute.return_value = []

        loan_id = 1
        repayment_schedule = calculate_repayment_schedule(loan_id)
        self.assertEqual(repayment_schedule, [])

if __name__ == '__main__':
    unittest.main()
