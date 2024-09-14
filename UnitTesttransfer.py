
import unittest
from unittest.mock import patch, mock_open, MonkeyPatch
from your_module import transfer_funds


class TestTransferFunds(unittest.TestCase):

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    @patch('your_module.print')
    def test_transfer_funds_valid(self, mock_print, mock_conn, mock_text, mock_engine):
        p_sender = 1
        p_receiver = 2
        p_amount = 10.0
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        mock_text.return_value = None
        transfer_funds(p_sender, p_receiver, p_amount)
        self.assertEqual(mock_conn.execute.call_count, 2)
        self.assertEqual(mock_conn.commit.call_count, 1)

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    @patch('your_module.print')
    def test_transfer_funds_sender_non_existent(self, mock_print, mock_conn, mock_text, mock_engine):
        p_sender = 100
        p_receiver = 2
        p_amount = 10.0
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        with self.assertRaises(Exception):
            transfer_funds(p_sender, p_receiver, p_amount)
        self.assertEqual(mock_conn.execute.call_count, 2)
        self.assertEqual(mock_conn.commit.call_count, 0)

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    @patch('your_module.print')
    def test_transfer_funds_receiver_non_existent(self, mock_print, mock_conn, mock_text, mock_engine):
        p_sender = 1
        p_receiver = 100
        p_amount = 10.0
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        with self.assertRaises(Exception):
            transfer_funds(p_sender, p_receiver, p_amount)
        self.assertEqual(mock_conn.execute.call_count, 2)
        self.assertEqual(mock_conn.commit.call_count, 0)

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    @patch('your_module.print')
    def test_transfer_funds_invalid_amount(self, mock_print, mock_conn, mock_text, mock_engine):
        p_sender = 1
        p_receiver = 2
        p_amount = 'ten'
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        with self.assertRaises(Exception):
            transfer_funds(p_sender, p_receiver, p_amount)
        self.assertEqual(mock_conn.execute.call_count, 0)
        self.assertEqual(mock_conn.commit.call_count, 0)

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    @patch('your_module.print')
    def test_transfer_funds_no_ddl_commands(self, mock_print, mock_conn, mock_text, mock_engine):
        p_sender = 1
        p_receiver = 2
        p_amount = 10.0
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        with patch('your_module.engine.connect') as mock_connect:
            with mock_connect.return_value as mock_connection:
                with mock_connection.cursor.return_value as mock_cursor:
                    mock_cursor.execute.return_value = None
                result = transfer_funds(p_sender, p_receiver, p_amount)
        self.assertEqual(mock_conn.execute.call_count, 2)
        self.assertEqual(mock_conn.commit.call_count, 1)
        self.assertIsNone(result)

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    @patch('your_module.print')
    def test_transfer_fundsDDL_commands(self, mock_print, mock_conn, mock_text, mock_engine):
        p_sender = 1
        p_receiver = 2
        p_amount = 10.0
        mock_conn.execute.return_value = None
        mock_conn.commit.return_value = None
        result = transfer_funds(p_sender, p_receiver, p_amount)
        self.assertIsNone(result)

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    @patch('your_module.print')
    def test_transfer_funds_execution_error(self, mock_print, mock_conn, mock_text, mock_engine):
        p_sender = 1
        p_receiver = 2
        p_amount = 10.0
        mock_conn.execute.side_effect = Exception('Error')
        with self.assertRaises(Exception):
            transfer_funds(p_sender, p_receiver, p_amount)
        self.assertEqual(mock_conn.execute.call_count, 2)
        self.assertEqual(mock_conn.commit.call_count, 0)

    @patch('your_module.engine')
    @patch('your_module.text')
    @patch('your_module.conn')
    @patch('your_module.print')
    def test_transfer_funds_commit_error(self, mock_print, mock_conn, mock_text, mock_engine):
        p_sender = 1
        p_receiver = 2
        p_amount = 10.0
        mock_conn.execute.return_value = None
        mock_conn.commit.side_effect = Exception('Error')
        try:
            transfer_funds(p_sender, p_receiver, p_amount)
        except Exception as e:
            self.assertEqual(str(e), 'Error')
        self.assertEqual(mock_conn.execute.call_count, 2)
        self.assertEqual(mock_conn.commit.call_count, 1)

if __name__ == '__main__':
    unittest.main()
