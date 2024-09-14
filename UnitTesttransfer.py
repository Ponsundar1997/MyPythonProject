
import unittest
from unittest.mock import patch, Mock
from your_module import transfer_funds

class TestTransferFunds(unittest.TestCase):
    @patch('your_module.engine')
    def test_transfer_funds_success(self, mock_engine):
        mock_engine.execute.return_value = None
        mock_engine.connect.return_value = Mock(commit=Mock(return_value=None), rollback=Mock(return_value=None))
        
        transfer_funds('sender_id', 'receiver_id', 100)
        
        mock_engine.execute.assert_called_with(text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), 
                                               p_sender='sender_id', p_amount=100)
        mock_engine.execute.assert_called_with(text("UPDATE accounts SET balance = balance + :p_amount WHERE id = :p_receiver"), 
                                               p_receiver='receiver_id', p_amount=100)
        mock_engine.connect().commit.assert_called_once()
    
    @patch('your_module.engine')
    def test_transfer_funds_no_sender_account(self, mock_engine):
        mock_engine.execute.return_value = None
        mock_engine.connect.return_value = Mock(commit=Mock(return_value=None), rollback=Mock(return_value=None))
        mock_engine.execute.return_value = None
        
        with self.assertRaises(Exception) as e:
            transfer_funds('sender_id', 'receiver_id', 100)
        
        mock_engine.execute.assert_called_with(text("SELECT 1 FROM accounts WHERE id = :p_sender"), p_sender='sender_id')
        self.assertEqual(str(e.exception), "Error: no sender account found")
    
    @patch('your_module.engine')
    def test_transfer_funds_no_receiver_account(self, mock_engine):
        mock_engine.execute.return_value = None
        mock_engine.connect.return_value = Mock(commit=Mock(return_value=None), rollback=Mock(return_value=None))
        mock_engine.execute.side_effect = [None, text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), None]
        
        with self.assertRaises(Exception) as e:
            transfer_funds('sender_id', 'receiver_id', 100)
        
        mock_engine.execute.assert_called_with(text("SELECT 1 FROM accounts WHERE id = :p_sender"), p_sender='sender_id')
        mock_engine.execute.assert_called_with(text("SELECT 1 FROM accounts WHERE id = :p_receiver"), 
                                               p_receiver='receiver_id')
        self.assertEqual(str(e.exception), "Error: no receiver account found")
    
    @patch('your_module.engine')
    def test_transfer_funds_insufficient_funds(self, mock_engine):
        mock_engine.execute.return_value = None
        mock_engine.connect.return_value = Mock(commit=Mock(return_value=None), rollback=Mock(return_value=None))
        mock_engine.execute.side_effect = [None, text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), Exception("Insufficient funds")]
        
        with self.assertRaises(Exception) as e:
            transfer_funds('sender_id', 'receiver_id', 1000)
        
        mock_engine.execute.assert_called_with(text("SELECT 1 FROM accounts WHERE id = :p_sender"), p_sender='sender_id')
        mock_engine.execute.assert_called_with(text("SELECT 1 FROM accounts WHERE id = :p_receiver"), 
                                               p_receiver='receiver_id')
        self.assertEqual(str(e.exception), "Error: insufficient funds")
    
    @patch('your_module.engine')
    def test_transfer_funds_other_exception(self, mock_engine):
        mock_engine.execute.return_value = None
        mock_engine.connect.return_value = Mock(commit=Mock(return_value=None), rollback=Mock(return_value=None))
        mock_engine.execute.side_effect = [None, text("UPDATE accounts SET balance = balance - :p_amount WHERE id = :p_sender"), Exception("Other exception")]
        
        with self.assertRaises(Exception) as e:
            transfer_funds('sender_id', 'receiver_id', 100)
        
        mock_engine.execute.assert_called_with(text("SELECT 1 FROM accounts WHERE id = :p_sender"), p_sender='sender_id')
        mock_engine.execute.assert_called_with(text("SELECT 1 FROM accounts WHERE id = :p_receiver"), 
                                               p_receiver='receiver_id')
        self.assertEqual(str(e.exception), "Error: Other exception")

if __name__ == '__main__':
    unittest.main()
