
import unittest
from unittest.mock import patch, Mock
from your_module import execute_transaction  # Import the function being tested

class TestExecuteTransaction(unittest.TestCase):
    @patch('your_module.engine')
    @patch('your_module.text')
    def test_execute_transaction(self, text_mock, engine_mock):
        # Mock the text function to return a mock cursor
        text_mock.return_value = Mock(return_value='SELECT 1')

        # Mock the engine to return a mock connection
        engine_mock.return_value = Mock(id=123, commit=Mock(), execute=Mock(return_value='Commited'))

        # Test the function with valid inputs
        sender = 1
        receiver = 2
        amount = 10
        execute_transaction(sender, receiver, amount)

        # Assert the expected queries were executed
        self.assertEqual(text_mock.call_args_list, [
            (update_sender, {}),
            (update_receiver, {})
        ])
        self.assertEqual(engine_mock.return_value.execute.call_args_list, [
            ((update_sender.replace('{sender}', str(sender)).replace('{amount}', str(amount)),), {}),
            ((update_receiver.replace('{receiver}', str(receiver)).replace('{amount}', str(amount)),), {})
        ])
        self.assertEqual(engine_mock.return_value.commit.call_count, 2)

    @patch('your_module.engine')
    @patch('your_module.text')
    def test_execute_transaction_invalid_sender(self, text_mock, engine_mock):
        # Mock the text function to return a mock cursor
        text_mock.return_value = Mock(return_value='SELECT 1')

        # Mock the engine to return a mock connection
        engine_mock.return_value = Mock(id=123, commit=Mock(), execute=Mock(return_value='Commited'))

        # Test the function with invalid sender
        sender = 'Invalid sender'
        receiver = 2
        amount = 10
        with self.assertRaises(ValueError):
            execute_transaction(sender, receiver, amount)

    @patch('your_module.engine')
    @patch('your_module.text')
    def test_execute_transaction_invalid_receiver(self, text_mock, engine_mock):
        # Mock the text function to return a mock cursor
        text_mock.return_value = Mock(return_value='SELECT 1')

        # Mock the engine to return a mock connection
        engine_mock.return_value = Mock(id=123, commit=Mock(), execute=Mock(return_value='Commited'))

        # Test the function with invalid receiver
        sender = 1
        receiver = 'Invalid receiver'
        amount = 10
        with self.assertRaises(ValueError):
            execute_transaction(sender, receiver, amount)

    @patch('your_module.engine')
    @patch('your_module.text')
    def test_execute_transaction_invalid_amount(self, text_mock, engine_mock):
        # Mock the text function to return a mock cursor
        text_mock.return_value = Mock(return_value='SELECT 1')

        # Mock the engine to return a mock connection
        engine_mock.return_value = Mock(id=123, commit=Mock(), execute=Mock(return_value='Commited'))

        # Test the function with invalid amount
        sender = 1
        receiver = 2
        amount = -10
        with self.assertRaises(ValueError):
            execute_transaction(sender, receiver, amount)

    @patch('your_module.engine')
    @patch('your_module.text')
    def test_execute_transaction_zero_amount(self, text_mock, engine_mock):
        # Mock the text function to return a mock cursor
        text_mock.return_value = Mock(return_value='SELECT 1')

        # Mock the engine to return a mock connection
        engine_mock.return_value = Mock(id=123, commit=Mock(), execute=Mock(return_value='Commited'))

        # Test the function with zero amount
        sender = 1
        receiver = 2
        amount = 0
        execute_transaction(sender, receiver, amount)

        # Assert the expected queries were not executed
        self.assertEqual(text_mock.call_args_list, [])
        self.assertEqual(engine_mock.return_value.execute.call_args_list, [])
        self.assertEqual(engine_mock.return_value.commit.call_count, 0)

if __name__ == '__main__':
    unittest.main()
