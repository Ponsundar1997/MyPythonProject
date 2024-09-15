
import unittest
from unittest.mock import patch, MagicMock
from your_module import transfer_amount
from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError
from sqlalchemy.engine import Engine

class TestTransferAmount(unittest.TestCase):

    def setUp(self):
        self.engine = Engine()
        self.patch_engine = patch('your_module.engine', self.engine)
        self.patch_engine.start()

    def tearDown(self):
        self.patch_engine.stop()

    def test_transfer_amount(self):
        with patch('your_module.text') as mock_text:
            query = mock_text.return_value
            query.execution_options.return_value.execute = MagicMock()
            transfer_amount(1, 2, 100.0)
            self.assertEqual(query.execution_options.return_value.execute.call_count, 2)

    def test_transfer_amount_execution_failure_first_query(self):
        with patch('your_module.text') as mock_text:
            query = mock_text.return_value
            query.execution_options.return_value.execute = MagicMock(side_effect=OperationalError())
            with self.assertRaises(OperationalError):
                transfer_amount(1, 2, 100.0)

    def test_transfer_amount_execution_failure_second_query(self):
        with patch('your_module.text') as mock_text:
            query = mock_text.return_value
            execute_mock = MagicMock(side_effect=[None, OperationalError()])
            query.execution_options.return_value.execute = execute_mock
            with self.assertRaises(OperationalError):
                transfer_amount(1, 2, 100.0)

    def test_transfer_amount_sender_receiver_same(self):
        with patch('your_module.text') as mock_text:
            query = mock_text.return_value
            query.execution_options.return_value.execute = MagicMock()
            transfer_amount(1, 1, 100.0)
            self.assertEqual(query.execution_options.return_value.execute.call_count, 2)

    def test_transfer_amount_zero_amount(self):
        with patch('your_module.text') as mock_text:
            query = mock_text.return_value
            query.execution_options.return_value.execute = MagicMock()
            transfer_amount(1, 2, 0.0)
            self.assertEqual(query.execution_options.return_value.execute.call_count, 2)

    def test_transfer_amount_negative_amount(self):
        with patch('your_module.text') as mock_text:
            query = mock_text.return_value
            query.execution_options.return_value.execute = MagicMock()
            transfer_amount(1, 2, -100.0)
            self.assertEqual(query.execution_options.return_value.execute.call_count, 2)

    def test_transfer_amount_int_amount(self):
        with patch('your_module.text') as mock_text:
            query = mock_text.return_value
            query.execution_options.return_value.execute = MagicMock()
            transfer_amount(1, 2, 100)
            self.assertEqual(query.execution_options.return_value.execute.call_count, 2)

    def test_transfer_amount_database_error(self):
        with patch('your_module.text') as mock_text:
            query = mock_text.return_value
            query.execution_options.return_value.execute = MagicMock(side_effect=DatabaseError())
            with self.assertRaises(DatabaseError):
                transfer_amount(1, 2, 100.0)

    def test_transfer_amount_invalid_type_error(self):
        with self.assertRaises(TypeError):
            transfer_amount('1', 2, 100.0)

    def test_transfer_amount_invalid_type_receiver(self):
        with self.assertRaises(TypeError):
            transfer_amount(1, '2', 100.0)

    def test_transfer_amount_invalid_type_amount(self):
        with self.assertRaises(TypeError):
            transfer_amount(1, 2, '100.0')

    if __name__ == '__main__':
        unittest.main()
