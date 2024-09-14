
import unittest
from unittest.mock import patch, Mock
from your_module import transfer_funds

class TestTransferFunds(unittest.TestCase):

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    def test_transfer_funds_positive_amount(self, mock_conn, mock_text, mock_engine):
        # Arrange
        sender_id = 1
        receiver_id = 2
        amount = 100
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        mock_conn.close.return_value = None
        mock_text.return_value = 'SELECT balance FROM accounts WHERE id = :sender'
        mock_conn.execute SIDE_EFFECT use mock_conn.execute.return_value

        # Act
        transfer_funds(sender_id, receiver_id, amount)

        # Assert
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        print(f"Sender's new balance: {sender_balance}")
        print(f"Receiver's new balance: {receiver_balance}")

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    def test_transfer_funds_negative_amount(self, mock_conn, mock_text, mock_engine):
        # Arrange
        sender_id = 1
        receiver_id = 2
        amount = -100
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        mock_conn.close.return_value = None
        mock_text.return_value = 'SELECT balance FROM accounts WHERE id = :sender'
        mock_conn.execute SIDE_EFFECT use mock_conn.execute.return_value

        # Act
        transfer_funds(sender_id, receiver_id, amount)

        # Assert
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        print(f"Sender's new balance: {sender_balance}")
        print(f"Receiver's new balance: {receiver_balance}")

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    def test_transfer_funds_zero_amount(self, mock_conn, mock_text, mock_engine):
        # Arrange
        sender_id = 1
        receiver_id = 2
        amount = 0
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        mock_conn.close.return_value = None
        mock_text.return_value = 'SELECT balance FROM accounts WHERE id = :sender'
        mock_conn.execute SIDE_EFFECT use mock_conn.execute.return_value

        # Act
        transfer_funds(sender_id, receiver_id, amount)

        # Assert
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        print(f"Sender's new balance: {sender_balance}")
        print(f"Receiver's new balance: {receiver_balance}")

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    def test_transfer_funds_sender_id_not_found(self, mock_conn, mock_text, mock_engine):
        # Arrange
        sender_id = 1
        receiver_id = 2
        amount = 100
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        mock_conn.close.return_value = None
        mock_text.return_value = 'SELECT balance FROM accounts WHERE id = :sender'
        mock_conn.execute SIDE_EFFECT use mock_conn.execute.return_value
        mock_conn.execute SIDE_EFFECT use raise Exception('sender not found')

        # Act and Assert
        with self.assertRaises(Exception):
            transfer_funds(sender_id, receiver_id, amount)
            mock_conn.execute.assert_called_once()
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
            print(f"Sender's new balance: {sender_balance}")
            print(f"Receiver's new balance: {receiver_balance}")

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    def test_transfer_funds_receiver_id_not_found(self, mock_conn, mock_text, mock_engine):
        # Arrange
        sender_id = 1
        receiver_id = 2
        amount = 100
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        mock_conn.close.return_value = None
        mock_text.return_value = 'SELECT balance FROM accounts WHERE id = :receiver'
        mock_conn.execute SIDE_EFFECT use mock_conn.execute.return_value
        mock_conn.execute SIDE_EFFECT use raise Exception('receiver not found')

        # Act and Assert
        with self.assertRaises(Exception):
            transfer_funds(sender_id, receiver_id, amount)
            mock_conn.execute.assert_called_once()
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
            print(f"Sender's new balance: {sender_balance}")
            print(f"Receiver's new balance: {receiver_balance}")

if __name__ == '__main__':
    unittest.main()
