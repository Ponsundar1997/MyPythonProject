
import unittest
from unittest.mock import patch, mock
from your_module import transfer_funds  # import the module

class TestTransferFunds(unittest.TestCase):
    @patch('your_module.engine')
    @patch('your_module.text')
    def test_transfer_funds_success(self, mock_text, mock_engine):
        mock_engine.execute.return_value = None
        transfer_funds(1, 2, 100)
        mock_text.assert_any_call("""
            UPDATE accounts 
            SET balance = balance - :amount 
            WHERE id = :sender
        """)
        mock_text.assert_any_call("""
            UPDATE accounts 
            SET balance = balance + :amount 
            WHERE id = :receiver
        """)
        mock_engine.execute.assert_any_call(query=mock_text(), parameters={'sender': 1, 'amount': 100})
        mock_engine.execute.assert_any_call(query=mock_text(), parameters={'receiver': 2, 'amount': 100})
        mock_engine.connect().commit.assert_called_once()

    @patch('your_module.engine')
    @patch('your_module.text')
    def test_transfer_funds_sender_notexists(self, mock_text, mock_engine):
        mock_engine.execute.side_effect = Exception('Sender not found')
        with self.assertRaises(Exception):
            transfer_funds(1, 2, 100)

    @patch('your_module.engine')
    @patch('your_module.text')
    def test_transfer_funds_receiver_notexists(self, mock_text, mock_engine):
        mock_engine.execute.side_effect = Exception('Receiver not found')
        with self.assertRaises(Exception):
            transfer_funds(1, 2, 100)

    @patch('your_module.engine')
    @patch('your_module.text')
    def test_transfer_funds_insufficient_balance(self, mock_text, mock_engine):
        mock_engine.execute.return_value = None
        transfer_funds(1, 2, 1000)  # sender balance is insufficient
        mock_text.assert_any_call("""
            UPDATE accounts 
            SET balance = balance - :amount 
            WHERE id = :sender
        """)
        mock_engine.execute.assert_any_call(query=mock_text(), parameters={'sender': 1, 'amount': 1000})
        self.assertFalse(mock_text.called)  # receiver update query not executed

    @patch('your_module.engine')
    @patch('your_module.text')
    def test_transfer_funds_negative_amount(self, mock_text, mock_engine):
        with self.assertRaises(ValueError):
            transfer_funds(1, 2, -10)

if __name__ == '__main__':
    unittest.main()
