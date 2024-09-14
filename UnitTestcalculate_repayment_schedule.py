
import unittest
import pandas as pd
from unittest.mock import patch
from your_module import calculate_repayment_schedule  # replace 'your_module' with the actual module name

class TestCalculateRepaymentSchedule(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_repayment_schedule_valid_loan_id(self, mock_engine):
        # Test valid loan ID
        loan_id = 1
        mock_engine.execute.return_value.fetchone.return_value = (10000, 5, 360, '2020-01-01')
        result = calculate_repayment_schedule(loan_id)
        self.assertIsInstance(result, pd.DataFrame)

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_invalid_loan_id(self, mock_engine):
        # Test invalid loan ID (returns None)
        loan_id = 999
        mock_engine.execute.return_value.fetchone.return_value = None
        result = calculate_repayment_schedule(loan_id)
        self.assertIsNone(result)

    @patch('your_module.engine')
    def test_calculate_repayment_schedule_query_error(self, mock_engine):
        # Test query execution error (returns None)
        loan_id = 1
        mock_engine.execute.return_value.fetchone.side_effect = Exception('Error')
        result = calculate_repayment_schedule(loan_id)
        self.assertIsNone(result)

    def test_calculate_repayment_schedule_output_format(self):
        # Test output format (repayment schedule DataFrame)
        loan_id = 1
        result = calculate_repayment_schedule(loan_id)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result.columns), 8)
        self.assertGreater(result.shape[0], 0)

    def test_calculate_repayment_schedule_calculations(self):
        # Test repayment schedule calculations (manually verify values)
        loan_id = 1
        result = calculate_repayment_schedule(loan_id)
        self.assertAlmostEqual(result['totalpayment'].values[0], 173.62, places=2)
        self.assertAlmostEqual(result['balance'].values[-1], 0, places=2)

if __name__ == '__main__':
    unittest.main()
