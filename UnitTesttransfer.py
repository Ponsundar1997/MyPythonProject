
import unittest
from unittest.mock import patch, Mock
from my_test_file import *  # Replace with the actual file name

class TestTransaction(unittest.TestCase):

    @patch('config.engine.url')
    @patch('sqlalchemy.create_engine')
    @patch('pandas as pd')
    def setUp(self, pd_mock, engine_mock, url_mock):
        self.engine = engine_mock
        self.url = url_mock
        self.sender = 1
        self.receiver = 2
        self.amount = 100

    def test_update_sender(self, pd_mock, engine_mock, url_mock):
        update_sender_sql = """
        update accounts 
        set balance = balance - :amount 
        where id = :sender;
        """
        result_sender = engine_mock.execute(text(update_sender_sql), sender=self.sender, amount=self.amount)
        self.assertEqual(result_sender, 'Update successful')

    def test_update_receiver(self, pd_mock, engine_mock, url_mock):
        update_receiver_sql = """
        update accounts 
        set balance = balance + :amount 
        where id = :receiver;
        """
        result_receiver = engine_mock.execute(text(update_receiver_sql), receiver=self.receiver, amount=self.amount)
        self.assertEqual(result_receiver, 'Update successful')

    def test_commit_changes(self, pd_mock, engine_mock, url_mock):
        conn = engine_mock
        result_commit = conn.execute("COMMIT;")
        self.assertEqual(result_commit, 'Commit successful')

    def test_drivername_postgresql(self, pd_mock, engine_mock, url_mock):
        url_mock.drivername = 'postgresql'
        conn = create_engine('postgresql://' + url_mock.username + ':' + url_mock.password + '@' + url_mock.host + ':' + str(url_mock.port) + '/' + url_mock.database)
        self.assertEqual(conn, engine_mock)

    def test_drivername_not_postgresql(self, pd_mock, engine_mock, url_mock):
        url_mock.drivername = 'not_postgresql'
        conn = create_engine('postgresql://' + url_mock.username + ':' + url_mock.password + '@' + url_mock.host + ':' + str(url_mock.port) + '/' + url_mock.database)
        self.assertEqual(conn, engine_mock)

if __name__ == '__main__':
    unittest.main()
