
import unittest
from unittest.mock import patch
from your_module import procedure

class TestProcedure(unittest.TestCase):
    @patch('your_module.engine')
    def test_procedure Successful_transation(self, mock_engine):
        sender_id = 1
        receiver_id = 2
        amount = 100

        mock_engine.connect().return_value = self._create_mock_connection()

        procedure(sender_id, receiver_id, amount)

        commit_call = mock_engine.connect().return_value.execute.call_args_list
        self.assertEqual(len(commit_call), 2)
        self.assertEqual(commit_call[0][0][0], update_sender)
        self.assertEqual(commit_call[1][0][0], update_receiver)
        self.assertEqual(mock_engine.connect().return_value.commit.call_count, 1)

    @patch('your_module.engine')
    def test_procedure_Rollback(self, mock_engine):
        sender_id = 1
        receiver_id = 2
        amount = 100

        mock_engine.connect().return_value = self._create_mock_connection()
        mock_engine.connect().return_value.execute.side_effect = Exception("Test Exception")
        
        with self.assertRaises(Exception) as err:
            procedure(sender_id, receiver_id, amount)

        self.assertEqual(err.exception.args[0], "Test Exception")
        commit_call = mock_engine.connect().return_value.execute.call_args_list
        self.assertEqual(len(commit_call), 2)
        self.assertEqual(commit_call[0][0][0], update_sender)
        self.assertEqual(commit_call[1][0][0], update_receiver)
        self.assertEqual(mock_engine.connect().return_value.rollback.call_count, 1)

    @patch('your_module.engine')
    def test_procedure_zero_amount(self, mock_engine):
        sender_id = 1
        receiver_id = 2
        amount = 0

        mock_engine.connect().return_value = self._create_mock_connection()

        procedure(sender_id, receiver_id, amount)

        commit_call = mock_engine.connect().return_value.execute.call_args_list
        self.assertEqual(len(commit_call), 0)
        self.assertEqual(mock_engine.connect().return_value.commit.call_count, 0)

    @patch('your_module.engine')
    def test_procedure_non_existent_sender(self, mock_engine):
        sender_id = 3
        receiver_id = 2
        amount = 100

        mock_engine.connect().return_value = self._create_mock_connection()

        with self.assertRaises(Exception) as err:
            procedure(sender_id, receiver_id, amount)

        self.assertEqual(err.exception.args[0], "Non-existent sender")
        rollback_call = mock_engine.connect().return_value.rollback.call_count
        self.assertEqual(rollback_call, 1)

    @patch('your_module.engine')
    def test_procedure_non_existent_receiver(self, mock_engine):
        sender_id = 1
        receiver_id = 3
        amount = 100

        mock_engine.connect().return_value = self._create_mock_connection()

        with self.assertRaises(Exception) as err:
            procedure(sender_id, receiver_id, amount)

        self.assertEqual(err.exception.args[0], "Non-existent receiver")
        rollback_call = mock_engine.connect().return_value.rollback.call_count
        self.assertEqual(rollback_call, 1)

    def _create_mock_connection(self):
        class MockConnection:
            def __init__(self):
                self.execute = self._execute

            def _execute(self, query):
                if query == update_sender:
                    return pd.DataFrame({"sender_id": [1]})
                elif query == update_receiver:
                    return pd.DataFrame({"receiver_id": [2]})
                else:
                    raise Exception("Invalid query")

        return MockConnection()

if __name__ == '__main__':
    unittest.main()
