
import unittest
from unittest.mock import patch
from your_module_name import calculate_loan_repayment  # Replace with your actual module name
import datetime

class TestCalculateLoanRepayment(unittest.TestCase):

    @patch('your_module_name.engine')
    def test_calculate_loan_repayment(self, engine_mock):
        engine_mock.connect.return_value = object()
        engine_mock.connect().execute.return_value = [(10000, 5, 60, datetime.date(2022, 1, 1))]
        
        calculate_loan_repayment(1)
        
        engine_mock.connect().execute.assert_called_once_with(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), loan_id={'loan_id': 1})
        insert_queries = [
            text(
                """INSERT INTO repaymentschedule 
                    (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
                    VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)
                """),
            text(
                """INSERT INTO repaymentschedule 
                    (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
                    VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)
                """),
            ...
        ]
        insert_queries[0].assert_called_once_with(loan_id=1, payment_number=1, payment_date=datetime.date(2022, 1, 1), principal_amount=..., interest_amount=..., monthly_payment=..., balance=...)
        insert_queries[1].assert_called_once_with(loan_id=1, payment_number=2, payment_date=datetime.date(2022, 2, 1), principal_amount=..., interest_amount=..., monthly_payment=..., balance=...)
        ...
        engine_mock.connect().commit.assert_called_once()
        engine_mock.connect().close.assert_called_once()

    @patch('your_module_name.engine')
    def test_calculate_loan_repayment_no_loans(self, engine_mock):
        engine_mock.connect.return_value = object()
        engine_mock.connect().execute.return_value = []
        
        self.assertRaises(ValueError, calculate_loan_repayment, 1)
        
        engine_mock.connect().execute.assert_called_once_with(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), loan_id={'loan_id': 1})

    @patch('your_module_name.engine')
    def test_calculate_loan_repayment_invalid_loan_id(self, engine_mock):
        engine_mock.connect.return_value = object()
        engine_mock.connect().execute.side_effect = [ObjectNotFound('Loan not found')]
        
        self.assertRaises(ObjectNotFound, calculate_loan_repayment, 1)
        
        engine_mock.connect().execute.assert_called_once_with(text("SELECT loanamount, interestrate, loanterm, startdate FROM loans WHERE loanid = :loan_id"), loan_id={'loan_id': 1})

if __name__ == '__main__':
    unittest.main()
