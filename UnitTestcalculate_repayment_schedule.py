
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_repayment_schedule  # Replace with the actual module name

class TestRepaymentSchedule(unittest.TestCase):
    @patch('your_module.engine.connect')  # Replace with the actual engine.connect function
    @patch('your_module.text')
    @patch('your_moduleCONN_EXECUTESQL_EXECUTE')
    @patch('your_moduleCONN_COMMIT')
    def test_calculate_repayment_schedule(self, conn_commit_mock, conn_execute_sql Execute_mock, text_mock, connect_mock):
        loan_details = (10000, 10.0, 360, '2022-01-01')  # Replace with expected loan details
        loan_id = 1
        monthly_interest_rate = loan_details[1] / 100 / 12
        monthly_payment = (loan_details[0] * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_details[2]))

        conn_execute_sql_Execute_mock.side_effect = [loan_details, []]  # Mocking database queries

        result = calculate_repayment_schedule(loan_id)

        self.assertEqual(len(result), 360)  # Check the number of repayments
        self.assertAlmostEqual(result[0]['total_payment'], monthly_payment, places=5)  # Check the total payment
        self.assertAlmostEqual(result[0]['balance'], 8449.69, places=2)  # Check the balance after first repayment

    @patch('your_module.engine.connect')  # Replace with the actual engine.connect function
    @patch('your_module.text')
    @patch('your_moduleCONN_EXECUTESQL_EXECUTE')
    @patch('your_moduleCONN_COMMIT')
    def test_calculate_repayment_schedule_invalid_loan_id(self, conn_commit_mock, conn_execute_sql_Execute_mock, text_mock, connect_mock):
        loan_id = 'invalid'
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

    @patch('your_module.engine.connect')  # Replace with the actual engine.connect function
    @patch('your_module.text')
    @patch('your_moduleCONN_EXECUTESQL_EXECUTE')
    @patch('your_moduleCONN_COMMIT')
    def test_calculate_repayment_schedule_missing_monthly_payment(self, conn_commit_mock, conn_execute_sql_Execute_mock, text_mock, connect_mock):
        loan_details = (10000, 10.0, 360, '2022-01-01')  # Replace with expected loan details
        loan_id = 1
        result = calculate_repayment_schedule(loan_id)
        self.assertAlmostEqual(result[0]['total_payment'], 285.72, places=2)  # Check the total payment

    @patch('your_module.engine.connect')  # Replace with the actual engine.connect function
    @patch('your_module.text')
    @patch('your_moduleCONN_EXECUTESQL_EXECUTE')
    @patch('your_moduleCONN_COMMIT')
    def test_calculate_repayment_schedule_loan_with_zero_balance(self, conn_commit_mock, conn_execute_sql_Execute_mock, text_mock, connect_mock):
        loan_details = (0, 10.0, 360, '2022-01-01')  # Replace with expected loan details
        loan_id = 1
        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(result, [])  # Check the repayments list is empty

    @patch('your_module.engine.connect')  # Replace with the actual engine.connect function
    @patch('your_module.text')
    @patch('your_moduleCONN.Executemany_executesql')  # Replace with the expected execute method
    @patch('your_moduleCONN_COMMIT')
    def test_calculate_repayment_schedule_multiple_loans(self, conn_commit_mock, execute_sql_Execute_mock, text_mock, connect_mock):
        loan_details = [(10000, 10.0, 360, '2022-01-01'), (20000, 10.0, 360, '2022-02-01')]  # Replace with expected loan details
        loan_id = [1, 2]
        result = calculate_repayment_schedule(loan_id)
        self.assertEqual(len(result), 2)  # Check the number of repayments
        self.assertAlmostEqual(result[0]['total_payment'], 285.72, places=2)  # Check the total payment

if __name__ == '__main__':
    unittest.main()
