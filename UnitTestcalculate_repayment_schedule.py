
import unittest
import pandas as pd
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        self.session = sessionmaker(bind=engine)()
        self.loan_details = {"loanamount": 10000, "interestrate": 6, "loanterm": 36, "startdate": "2022-01-01"}
        self.loan_id = 123
        self.engine = engine 

    def test_calculate_repayment_schedule(self):
        # Test with valid loan details
        result = calculate_repayment_schedule(self.loan_id)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 36)

        # Test with loanid not in the database
        result = calculate_repayment_schedule(999)
        self.assertIsNone(result)

        # Test with missing values in loan details
        missing_values_loan_details = {"loanamount": None, "interestrate": 6, "loanterm": 36, "startdate": "2022-01-01"}
        result = calculate_repayment_schedule(self.loan_id)
        self.assertIsNone(result)

        # Test with invalid interest rate
        invalid_interest_rate = {"loanamount": 10000, "interestrate": -1, "loanterm": 36, "startdate": "2022-01-01"}
        result = calculate_repayment_schedule(self.loan_id)
        self.assertIsNone(result)

        # Test with loan term less than 1
        invalid_loan_term = {"loanamount": 10000, "interestrate": 6, "loanterm": 0, "startdate": "2022-01-01"}
        result = calculate_repayment_schedule(self.loan_id)
        self.assertIsNone(result)

        # Test with start date in the future
        invalid_start_date = {"loanamount": 10000, "interestrate": 6, "loanterm": 36, "startdate": "2050-01-01"}
        result = calculate_repayment_schedule(self.loan_id)
        self.assertIsNone(result)

        # Test with start date less than today
        invalid_start_date = {"loanamount": 10000, "interestrate": 6, "loanterm": 36, "startdate": "2021-01-01"}
        result = calculate_repayment_schedule(self.loan_id)
        self.assertIsNone(result)

    def tearDown(self):
        self.session.close()

if __name__ == '__main__':
    unittest.main()
