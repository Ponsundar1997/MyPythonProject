
import unittest
from your_module import transfer  # Replace 'your_module' with the actual name of the module where the function is defined

class TestTransfer(unittest.TestCase):

    def test_transfer succeeds(self):
        # Arrange
        amount = 100
        sender = 1
        receiver = 2
        expected_balance_sender = 0
        expected_balance_receiver = 100

        # Act
        result = transfer(amount, sender, receiver)

        # Assert
        self.assertEqual(result[0], expected_balance_sender)
        self.assertEqual(result[1], expected_balance_receiver)

    def test_transfer insufficient sender(self):
        # Arrange
        amount = 1000
        sender = 1
        receiver = 2
        expected_balance_sender = 0
        expected_balance_receiver = 0

        # Act
        result = transfer(amount, sender, receiver)

        # Assert
        self.assertEqual(result[0], expected_balance_sender)
        self.assertEqual(result[1], expected_balance_receiver)

    def test_transfer no receiver (receiver does not exist in database) (this might not work in real life due to DB constraints):
        # Arrange
        amount = 100
        sender = 1
        receiver = 3  # receiver does not exist in db
        expected_balance_sender = 0
        expected_balance_receiver = 0

        # Act
        result = transfer(amount, sender, receiver)

        # Assert
        self.assertEqual(result[0], expected_balance_sender)
        self.assertEqual(result[1], expected_balance_receiver)

    def test_transfer receiver already has balance (receiver now has more than the sender) (this is not how a real bank works, but a test case):
        # Arrange
        amount = 1000
        sender = 1
        receiver = 2
        initial_balance_receiver = 500  # receiver had 500 initially
        expected_balance_sender = -1000  # sender loses 1000, receiver gains 900 (initial balance + 1000 - 100)
        expected_balance_receiver = 1500  # receiver now has 1500

        # Act
        result = transfer(amount, sender, receiver)

        # Assert
        self.assertEqual(result[0], expected_balance_sender)
        self.assertEqual(result[1], expected_balance_receiver)

    def test_transfer zero amount (does not change anything):
        # Arrange
        amount = 0
        sender = 1
        receiver = 2
        expected_balance_sender = 100
        expected_balance_receiver = 200

        # Act
        result = transfer(amount, sender, receiver)

        # Assert
        self.assertEqual(result[0], expected_balance_sender)
        self.assertEqual(result[1], expected_balance_receiver)

    def test_transfer negative amount (will throw error):
        with self.assertRaises(Exception):
            # Arrange
            amount = -100
            sender = 1
            receiver = 2
            # Act
            transfer(amount, sender, receiver)

    def test_transfer sender and receiver ids are None (will throw error):
        with self.assertRaises(Exception):
            # Arrange
            amount = 100
            sender = None
            receiver = None
            # Act
            transfer(amount, sender, receiver)

    def test_transfer sender and receiver ids are not integers (will throw error):
        with self.assertRaises(Exception):
            # Arrange
            amount = 100
            sender = "John"
            receiver = "Jane"
            # Act
            transfer(amount, sender, receiver)

if __name__ == '__main__':
    unittest.main()
