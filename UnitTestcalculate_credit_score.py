
import unittest
from unittest.mock import MagicMock
from your_module import update_customer_credit_score

class TestUpdateCustomerCreditScore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        cls.conn = cls.engine.connect()

    def setUp(self):
        selfMocks = {
            'engine': cls.engine,
            'conn': self.conn
        }
        self.update_customer_credit_score = update_customer_credit_score
        self.update_customer_credit_score.configure(**selfMocks)

    def test_update_customer_credit_score_positive_defaults(self):
        selfMocks['conn'].execute = MagicMock(return_value=[1, 100, 10000, 0])
        result = self.update_customer_credit_score(1)
        self.assertEqual(result, 550)

    def test_update_customer_credit_score_negative_defaults(self):
        selfMocks['conn'].execute = MagicMock(return_value=[-1, -100, -10000, 0])
        result = self.update_customer_credit_score(1)
        self.assertEqual(result, 500)

    def test_update_customer_credit_score_nonzero_loan_amount(self):
        selfMocks['conn'].execute = MagicMock(return_value=[100, 50, 0, 0])
        result = self.update_customer_credit_score(1)
        self.assertEqual(result, 500)

    def test_update_customer_credit_score_zero_loan_amount(self):
        selfMocks['conn'].execute = MagicMock(return_value=[0, 0, 0, 0])
        result = self.update_customer_credit_score(1)
        self.assertEqual(result, 700)

    def test_update_customer_credit_score_credit_card_balance_zero(self):
        selfMocks['conn'].execute = MagicMock(return_value=[0, 0, 0, 0])
        result = self.update_customer_credit_score(1)
        self.assertEqual(result, 600)

    def test_update_customer_credit_score_large_credit_card_balance(self):
        selfMocks['conn'].execute = MagicMock(return_value=[0, 0, 10000, 0])
        result = self.update_customer_credit_score(1)
        self.assertEqual(result, 350)

    def test_update_customer_credit_score_late_payments(self):
        selfMocks['conn'].execute = MagicMock(return_value=[0, 0, 0, 3])
        result = self.update_customer_credit_score(1)
        self.assertEqual(result, 450)

    def test_update_customer_credit_score_low_score_alert(self):
        selfMocks['conn'].execute = MagicMock(return_value=[0, 0, 0, 10])
        result = self.update_customer_credit_score(1)
        self.assertEqual(result, 300)

if __name__ == '__main__':
    unittest.main()
