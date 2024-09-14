
import unittest
from unittest.mock import patch, mock_open, Mock
from your_module import transfer_amount  # replace 'your_module' with the actual name of your module

class TestTransferAmount(unittest.TestCase):

    @patch('your_module.engine')
    def test_transfer_amount_success(self, mock_engine):
        conn = mock_engine.connect.return_value
        conn.execute.return_value = None
        conn.commit.return_value = None
        conn.close.return_value = None

        p_sender = 1
        p_receiver = 2
        p_amount = 10

        transfer_amount(p_sender, p_receiver, p_amount)

        conn.execute.assert_has_calls([
            mock.call(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), p_amount=p_amount, p_sender=p_sender),
            mock.call(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), p_amount=p_amount, p_receiver=p_receiver),
        ], any_order=True)

    @patch('your_module.engine')
    def test_transfer_amount_sender_not_found(self, mock_engine):
        conn = mock_engine.connect.return_value
        conn.execute().execution_options.return_value = None
        conn.execute.side_effect = [Exception('Sender account not found')]

        p_sender = 1
        p_receiver = 2
        p_amount = 10

        with self.assertRaises(Exception):
            transfer_amount(p_sender, p_receiver, p_amount)

        conn.execute.assert_called_once_with(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), p_amount=p_amount, p_sender=p_sender)

    @patch('your_module.engine')
    def test_transfer_amount_receiver_not_found(self, mock_engine):
        conn = mock_engine.connect.return_value
        conn.execute().execution_options.return_value = None
        conn.execute.side_effect = [Exception('Receiver account not found')]

        p_sender = 1
        p_receiver = 2
        p_amount = 10

        with self.assertRaises(Exception):
            transfer_amount(p_sender, p_receiver, p_amount)

        conn.execute.assert_called_once_with(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), p_amount=p_amount, p_receiver=p_receiver)

    @patch('your_module.engine')
    def test_transfer_amount_database_error(self, mock_engine):
        conn = mock_engine.connect.return_value
        conn.execute().execution_options.return_value = None
        conn.execute.side_effect = [Exception('Database error')]

        p_sender = 1
        p_receiver = 2
        p_amount = 10

        with self.assertRaises(Exception):
            transfer_amount(p_sender, p_receiver, p_amount)

        conn.execute.assert_called_once_with(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), p_amount=p_amount, p_sender=p_sender)
        conn.rollback.assert_called_once_with()

    @patch('your_module.engine')
    def test_transfer_amount_positive_amount(self, mock_engine):
        conn = mock_engine.connect.return_value
        conn.execute.return_value = None
        conn.commit.return_value = None
        conn.close.return_value = None

        p_sender = 1
        p_receiver = 2
        p_amount = 10

        transfer_amount(p_sender, p_receiver, p_amount)

        conn.execute.assert_has_calls([
            mock.call(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), p_amount=p_amount, p_sender=p_sender),
            mock.call(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), p_amount=p_amount, p_receiver=p_receiver),
        ], any_order=True)

    @patch('your_module.engine')
    def test_transfer_amount_negative_amount(self, mock_engine):
        conn = mock_engine.connect.return_value
        conn.execute.return_value = None
        conn.commit.return_value = None
        conn.close.return_value = None

        p_sender = 1
        p_receiver = 2
        p_amount = -10

        transfer_amount(p_sender, p_receiver, p_amount)

        conn.execute.assert_has_calls([
            mock.call(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), p_amount=p_amount, p_sender=p_sender),
            mock.call(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), p_amount=p_amount, p_receiver=p_receiver),
        ], any_order=True)

if __name__ == '__main__':
    unittest.main()
