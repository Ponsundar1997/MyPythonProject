Python
import unittest
from unittest.mock import patch
from your_module import transfer_funds

class TestTransferFunds(unittest.TestCase):

    @patch('your_module.engine')
    def test_transfer_funds(self, engine_mock):
        transfer_funds(1, 2, 100.0)

        engine_mock.execute.assert_called_with(text("begin"))
        engine_mock.connect.assert_called_once()
        connection_mock = engine_mock.connect.return_value.__enter__.return_value
        connection_mock.execute.assert_any_call(text("update accounts set balance = balance - :amount where id = :sender").bindparams(sender=1, amount=100.0))
        connection_mock.execute.assert_any_call(text("update accounts set balance = balance + :amount where id = :receiver").bindparams(receiver=2, amount=100.0))
        engine_mock.execute.assert_called_with(text("commit"))

    @patch('your_module.engine')
    def test_transfer_funds_error(self, engine_mock):
        with self.assertRaises(Exception):
            transfer_funds(1, 1, 100.0)

    @patch('your_module.engine')
    def test_transfer_funds_sender_not_found(self, engine_mock):
        engine_mock.connect.return_value.execute.side_effect = Exception("Error message")
        with self.assertRaises(Exception):
            transfer_funds(1, 2, 100.0)

    @patch('your_module.engine')
    def test_transfer_funds_receiver_not_found(self, engine_mock):
        engine_mock.connect.return_value.execute.side_effect = Exception("Error message")
        with self.assertRaises(Exception):
            transfer_funds(1, 2, 100.0)

if __name__ == '__main__':
    unittest.main()
