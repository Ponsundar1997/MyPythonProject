
import unittest
import pandas as pd
from your_module import calculate_repayment_schedule  # replace 'your_module' with the actual name of your module/file

class TestCalculateRepaymentSchedule(unittest.TestCase):

    def setUp(self):
        # Create a test engine
        self.engine = create_engine('postgresql://user:password@host:port/dbname')

    def test_calculate_repayment_schedule(self):
        # Given
        loan_id = 1
        expected_output = pd.DataFrame({'paymentnumber': [1, 2, 3, 4], 'paymentdate': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01'],
                                        'principalamount': ['100.0', '200.0', '300.0', '400.0'],
                                        'interestamount': ['50.0', '40.0', '30.0', '20.0'],
                                        'totalpayment': ['150.0', '240.0', '330.0', '420.0'],
                                        'balance': ['800.0', '600.0', '300.0', '0.0']})

        # When
        result = calculate_repayment_schedule(loan_id)

        # Then
        self.assertTrue(isinstance(result, list) and len(result) > 0)
        self.assertEqual(len(result), expected_output.shape[0])
        for row in result:
            self.assertTrue(all(exp_val in str(row) for exp_val in expected_output.iloc[0]))

    def test_calculate_repayment_schedule_invalid_loan_id(self):
        # Given
        loan_id = 0  # or any other invalid loan_id

        # When
        with self.assertRaises(TypeError):
            calculate_repayment_schedule(loan_id)

    def test_calculate_repayment_schedule_non_numeric_loan_id(self):
        # Given
        loan_id = 'abc'  # or any other non-numeric value

        # When
        with self.assertRaises(TypeError):
            calculate_repayment_schedule(loan_id)

    def test_calculate_repayment_schedule_zero_loan_amount(self):
        # Given
        loan_id = 1
        initial_balance = 0

        # When
        with self.assertRaises(ZeroDivisionError):
            calculate_repayment_schedule(loan_id)

    def tearDown(self):
        # Clean up
        self.engine.execute("DROP TABLE IF EXISTS repaymentschedule")
        self.engine.execute("DROP TABLE IF EXISTS loans")

if __name__ == '__main__':
    unittest.main()
