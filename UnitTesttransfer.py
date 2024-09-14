
import unittest
from transfer_between_accounts import transfer_between_accounts

class TestTransferBetweenAccounts(unittest.TestCase):

    def setUp(self):
        engine.execute("TRUNCATE TABLE accounts")
        engine.execute(text("INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 200)"))

    def testTransferPositiveAmount(self):
        transfer_between_accounts(1, 2, 20)
        sender = pd.read_sql_query("SELECT * FROM accounts WHERE id = 1", engine).balance.iloc[0]
        receiver = pd.read_sql_query("SELECT * FROM accounts WHERE id = 2", engine).balance.iloc[0]
        self.assertEqual(sender, 80)
        self.assertEqual(receiver, 220)

    def testTransferNegativeAmount(self):
        transfer_between_accounts(1, 2, -20)
        sender = pd.read_sql_query("SELECT * FROM accounts WHERE id = 1", engine).balance.iloc[0]
        receiver = pd.read_sql_query("SELECT * FROM accounts WHERE id = 2", engine).balance.iloc[0]
        self.assertEqual(sender, 120)
        self.assertEqual(receiver, 220)

    def testTransferZeroAmount(self):
        transfer_between_accounts(1, 2, 0)
        sender = pd.read_sql_query("SELECT * FROM accounts WHERE id = 1", engine).balance.iloc[0]
        receiver = pd.read_sql_query("SELECT * FROM accounts WHERE id = 2", engine).balance.iloc[0]
        self.assertEqual(sender, 100)
        self.assertEqual(receiver, 200)

    def testTransferSameAccount(self):
        with self.assertRaises(ValueError):
            transfer_between_accounts(1, 1, 20)

    def testTransferInvalidSenderId(self):
        with self.assertRaises(ValueError):
            transfer_between_accounts(3, 2, 20)

    def testTransferInvalidReceiverId(self):
        with self.assertRaises(ValueError):
            transfer_between_accounts(1, 3, 20)

    def tearDown(self):
        engine.execute("TRUNCATE TABLE accounts")

if __name__ == '__main__':
    unittest.main()
