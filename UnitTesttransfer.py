
import unittest
from your_module import transfer_funds
import tempfile
import shutil
import os

class TestTransferFunds(unittest.TestCase):
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.engine = sa.create_engine('sqlite:///:memory:')
        with self.engine.connect() as conn:
            conn.execute(text('''
                create table accounts (
                    id integer primary key,
                    balance integer
                );
            '''))
            conn.execute(text('insert into accounts (id, balance) values (1, 100)'))
            conn.execute(text('insert into accounts (id, balance) values (2, 50)'))

    def teardown_method(self):
        shutil.rmtree(self.temp_dir)

    def test_transfer_funds_positive(self):
        transfer_funds(1, 2, 20)
        with self.engine.connect() as conn:
            result = conn.execute(text('select * from accounts'))
            self.assertEqual(list(result), [(1, 80), (2, 70)])

    def test_transfer_funds_negative(self):
        transfer_funds(1, 2, -10)
        with self.engine.connect() as conn:
            result = conn.execute(text('select * from accounts'))
            self.assertEqual(list(result), [(1, 90), (2, 60)])

    def test_transfer_funds_zero(self):
        transfer_funds(1, 2, 0)
        with self.engine.connect() as conn:
            result = conn.execute(text('select * from accounts'))
            self.assertEqual(list(result), [(1, 100), (2, 50)])

    def test_transfer_funds_invalid_sender(self):
        with self.assertRaises(ValueError):
            transfer_funds(-1, 2, 20)

    def test_transfer_funds_invalid_receiver(self):
        with self.assertRaises(ValueError):
            transfer_funds(1, -2, 20)

    def test_transfer_funds_invalid_amount(self):
        with self.assertRaises(ValueError):
            transfer_funds(1, 2, -100)

    def test_transfer_funds_non_existent_sender(self):
        with self.engine.connect() as conn:
            conn.execute(text('delete from accounts where id = 1'))
        with self.assertRaises(KeyError):
            transfer_funds(1, 2, 20)

    def test_transfer_funds_non_existent_receiver(self):
        with self.engine.connect() as conn:
            conn.execute(text('delete from accounts where id = 2'))
        with self.assertRaises(KeyError):
            transfer_funds(1, 2, 20)

if __name__ == '__main__':
    unittest.main()
