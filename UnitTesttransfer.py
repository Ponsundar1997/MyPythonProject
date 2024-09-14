
import unittest
from unittest.mock import patch
from your_module import transfer_amount
import pandas as pd
from config import engine
import sqlalchemy

class TestTransferAmount(unittest.TestCase):

    @patch('sqlalchemy.text')
    def test_transfer_amount_success(self, mock_sqlalchemy_text):
        # Arrange
        sender_id = 1
        receiver_id = 2
        amount = 100
        accounts_df = pd.DataFrame({'id': [1, 2], 'balance': [100, 200]})
        accounts_df.to_sql('accounts', engine, if_exists='replace', index=False)

        # Act
        transfer_amount(sender_id, receiver_id, amount)
        result = pd.read_sql_table('accounts', engine)

        # Assert
        self.assertEqual(result.loc[0, 'balance'], 0)
        self.assertEqual(result.loc[1, 'balance'], 300)
        self.assertTrue(mock_sqlalchemy_text.called)

    @patch('sqlalchemy.text')
    def test_transfer_amount_invalid_sender(self, mock_sqlalchemy_text):
        # Arrange
        sender_id = 3
        receiver_id = 2
        amount = 100
        accounts_df = pd.DataFrame({'id': [1, 2], 'balance': [100, 200]})
        accounts_df.to_sql('accounts', engine, if_exists='replace', index=False)

        # Act
        transfer_amount(sender_id, receiver_id, amount)

        # Assert
        result = pd.read_sql_table('accounts', engine)
        self.assertEqual(result.loc[0, 'balance'], 100)
        self.assertEqual(result.loc[1, 'balance'], 200)
        self.assertTrue(mock_sqlalchemy_text.called)

    @patch('sqlalchemy.text')
    def test_transfer_amount_invalid_receiver(self, mock_sqlalchemy_text):
        # Arrange
        sender_id = 1
        receiver_id = 3
        amount = 100
        accounts_df = pd.DataFrame({'id': [1, 2], 'balance': [100, 200]})
        accounts_df.to_sql('accounts', engine, if_exists='replace', index=False)

        # Act
        transfer_amount(sender_id, receiver_id, amount)

        # Assert
        result = pd.read_sql_table('accounts', engine)
        self.assertEqual(result.loc[0, 'balance'], 100)
        self.assertEqual(result.loc[1, 'balance'], 200)
        self.assertTrue(mock_sqlalchemy_text.called)

    @patch('sqlalchemy.text')
    def test_transfer_amount_insufficient_balance(self, mock_sqlalchemy_text):
        # Arrange
        sender_id = 1
        receiver_id = 2
        amount = 1000
        accounts_df = pd.DataFrame({'id': [1, 2], 'balance': [100, 200]})
        accounts_df.to_sql('accounts', engine, if_exists='replace', index=False)

        # Act
        transfer_amount(sender_id, receiver_id, amount)

        # Assert
        result = pd.read_sql_table('accounts', engine)
        self.assertEqual(result.loc[0, 'balance'], 100)
        self.assertEqual(result.loc[1, 'balance'], 200)
        self.assertTrue(mock_sqlalchemy_text.called)

    def test_transfer_amount_engine_error(self):
        # Arrange
        sender_id = 1
        receiver_id = 2
        amount = 100
        accounts_df = pd.DataFrame({'id': [1, 2], 'balance': [100, 200]})
        accounts_df.to_sql('accounts', engine, if_exists='replace', index=False)
        engine.execute = lambda query: None

        # Act
        transfer_amount(sender_id, receiver_id, amount)

        # Assert
        result = pd.read_sql_table('accounts', engine)
        self.assertEqual(result.loc[0, 'balance'], 100)
        self.assertEqual(result.loc[1, 'balance'], 200)

if __name__ == '__main__':
    unittest.main()
