
import unittest
import mock
from unittest.mock import patch, MagicMock
from sqlalchemy.sql import text
from your_module import calculate_credit_score  # Import the function you want to test

class TestCalculateCreditScore(unittest.TestCase):

    @patch('your_module.engine')
    def test_calculate_credit_score(self, mock_engine):
        # Arrange
        mock_connection = mock_engine.connect.return_value.__enter__.return_value
        mock_connection.execute.return_value.fetchone.side_effect = [
            [1000, 500, 500],
            [1000],
            [2],
            None,  # fetchone for payment return no value, then next three fetch for alerts return no value
            None,
            None,
        ]
        customer_id = 123

        # Act
        calculate_credit_score(customer_id)

        # Assert
        self.assertEqual(mock_connection.execute.call_count, 7)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COUNT_payments AS late_payment_count
            FROM (
                SELECT COUNT(*) AS COUNT_payments
                FROM payments
                WHERE payments.customer_id = :customer_id AND status = 'Late'
            ) AS subquery;
        """), customer_id=customer_id)
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('your_module.engine')
    def test_calculate_credit_score_no_loans(self, mock_engine):
        # Arrange
        mock_connection = mock_engine.connect.return_value.__enter__.return_value
        mock_connection.execute.return_value.fetchone.side_effect = [
            None,
            [1000],
            [2],
        ]
        customer_id = 123

        # Act
        calculate_credit_score(customer_id)

        # Assert
        self.assertEqual(mock_connection.execute.call_count, 6)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COUNT_payments AS late_payment_count
            FROM (
                SELECT COUNT(*) AS COUNT_payments
                FROM payments
                WHERE payments.customer_id = :customer_id AND status = 'Late'
            ) AS subquery;
        """), customer_id=customer_id)
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('your_module.engine')
    def test_calculate_credit_score_no_credit_cards(self, mock_engine):
        # Arrange
        mock_connection = mock_engine.connect.return_value.__enter__.return_value
        mock_connection.execute.return_value.fetchone.side_effect = [
            [1000, 500, 500],
            None,
            [2],
        ]
        customer_id = 123

        # Act
        calculate_credit_score(customer_id)

        # Assert
        self.assertEqual(mock_connection.execute.call_count, 6)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COUNT_payments AS late_payment_count
            FROM (
                SELECT COUNT(*) AS COUNT_payments
                FROM payments
                WHERE payments.customer_id = :customer_id AND status = 'Late'
            ) AS subquery;
        """), customer_id=customer_id)
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('your_module.engine')
    def test_calculate_credit_score_no_late_payments(self, mock_engine):
        # Arrange
        mock_connection = mock_engine.connect.return_value.__enter__.return_value
        mock_connection.execute.return_value.fetchone.side_effect = [
            [1000, 500, 500],
            [1000],
            None,
        ]
        customer_id = 123

        # Act
        calculate_credit_score(customer_id)

        # Assert
        self.assertEqual(mock_connection.execute.call_count, 6)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COUNT_payments AS late_payment_count
            FROM (
                SELECT COUNT(*) AS COUNT_payments
                FROM payments
                WHERE payments.customer_id = :customer_id AND status = 'Late'
            ) AS subquery;
        """), customer_id=customer_id)
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('your_module.engine')
    def test_calculate_credit_score_low_score(self, mock_engine):
        # Arrange
        mock_connection = mock_engine.connect.return_value.__enter__.return_value
        mock_connection.execute.return_value.fetchone.side_effect = [
            [0, 0, 0],
            [1000],
            [2],
        ]
        customer_id = 123

        # Act
        calculate_credit_score(customer_id)

        # Assert
        self.assertEqual(mock_connection.execute.call_count, 6)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COUNT_payments AS late_payment_count
            FROM (
                SELECT COUNT(*) AS COUNT_payments
                FROM payments
                WHERE payments.customer_id = :customer_id AND status = 'Late'
            ) AS subquery;
        """), customer_id=customer_id)
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('your_module.engine')
    def test_calculate_credit_score_connection_close(self, mock_engine):
        # Arrange
        mock_connection = mock_engine.connect.return_value.__enter__.return_value
        mock_connection.execute.return_value.fetchone.side_effect = [
            [1000, 500, 500],
            [1000],
            [2],
        ]
        customer_id = 123
        mock_connection.close.side_effect = Exception('Mock exception')

        # Act
        with self.assertRaises(Exception):
            calculate_credit_score(customer_id)

        # Assert
        self.assertEqual(mock_connection.execute.call_count, 6)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), 
                   COALESCE(ROUND(SUM(repayment_amount), 2), 0), 
                   COALESCE(ROUND(SUM(outstanding_balance), 2), 0)
            FROM loans
            WHERE loans.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COALESCE(ROUND(SUM(balance), 2), 0)
            FROM credit_cards
            WHERE credit_cards.customer_id = :customer_id;
        """), customer_id=customer_id)
        mock_connection.execute.assert_any_call(text("""
            SELECT COUNT_payments AS late_payment_count
            FROM (
                SELECT COUNT(*) AS COUNT_payments
                FROM payments
                WHERE payments.customer_id = :customer_id AND status = 'Late'
            ) AS subquery;
        """), customer_id=customer_id)
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
