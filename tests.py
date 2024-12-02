import unittest
from unittest.mock import Mock
from payment_processor import (
    PaymentProcessor,
    TransactionResult,
    TransactionStatus,
    NetworkException,
    PaymentException,
    RefundException,
    PaymentGateway,
)


class TestPaymentProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_gateway = Mock(spec=PaymentGateway)
        self.processor = PaymentProcessor(self.mock_gateway)

    def test_process_payment_success(self):
        user_id = "user123"
        amount = 100.0
        transaction_id = "txn123"

        self.mock_gateway.charge.return_value = TransactionResult(
            transaction_id, TransactionStatus.COMPLETED, ""
        )

        result = self.processor.process_payment(user_id, amount)

        self.assertTrue(result.status == TransactionStatus.COMPLETED)
        self.assertEqual(result.transaction_id, transaction_id)
        self.assertEqual(result.message, "Payment processed successfully")

    def test_process_payment_insufficient_funds(self):
        user_id = "user123"
        amount = 100.0

        self.mock_gateway.charge.side_effect = PaymentException("Insufficient funds")

        result = self.processor.process_payment(user_id, amount)

        self.assertTrue(result.status == TransactionStatus.FAILED)
        self.assertEqual(result.message, "Insufficient funds")

    def test_process_payment_network_exception(self):
        user_id = "user123"
        amount = 100.0

        self.mock_gateway.charge.side_effect = NetworkException("Network error")

        result = self.processor.process_payment(user_id, amount)

        self.assertTrue(result.status == TransactionStatus.FAILED)
        self.assertEqual(result.message, "Network error")

    def test_process_payment_invalid_amount(self):
        with self.assertRaises(ValueError) as context:
            self.processor.process_payment("user123", -50)
        self.assertEqual(str(context.exception), "Amount must be greater than zero")

    def test_process_payment_empty_user_id(self):
        with self.assertRaises(ValueError) as context:
            self.processor.process_payment("", 100.0)
        self.assertEqual(str(context.exception), "User ID must not be empty")

    def test_refund_payment_success(self):
        transaction_id = "txn123"
        refund_id = "refund123"

        self.mock_gateway.refund.return_value = TransactionResult(
            refund_id, TransactionStatus.COMPLETED, ""
        )

        result = self.processor.refund_payment(transaction_id)

        self.assertTrue(result.status == TransactionStatus.COMPLETED)
        self.assertEqual(result.transaction_id, refund_id)
        self.assertEqual(result.message, "Payment refunded successfully")

    def test_refund_payment_non_existent_transaction(self):
        transaction_id = "txn123"

        self.mock_gateway.refund.side_effect = RefundException(
            "Transaction does not exist"
        )

        result = self.processor.refund_payment(transaction_id)

        self.assertTrue(result.status == TransactionStatus.FAILED)
        self.assertEqual(result.message, "Transaction does not exist")

    def test_refund_payment_network_exception(self):
        transaction_id = "txn123"

        self.mock_gateway.refund.side_effect = NetworkException("Network error")

        result = self.processor.refund_payment(transaction_id)

        self.assertTrue(result.status == TransactionStatus.FAILED)
        self.assertEqual(result.message, "Network error")

    def test_refund_payment_empty_transaction_id(self):
        with self.assertRaises(ValueError) as context:
            self.processor.refund_payment("")
        self.assertEqual(str(context.exception), "Transaction ID must not be empty")

    def test_get_payment_status_success(self):
        transaction_id = "txn123"
        self.mock_gateway.getStatus.return_value = TransactionStatus.COMPLETED

        status = self.processor.get_payment_status(transaction_id)

        self.assertEqual(status, TransactionStatus.COMPLETED)

    def test_get_payment_status_non_existent_transaction(self):
        transaction_id = "txn123"

        self.mock_gateway.getStatus.side_effect = NetworkException(
            "Transaction does not exist"
        )

        with self.assertRaises(NetworkException):
            self.processor.get_payment_status(transaction_id)

    def test_get_payment_status_network_exception(self):
        transaction_id = "txn123"

        self.mock_gateway.getStatus.side_effect = NetworkException("Network error")

        with self.assertRaises(NetworkException):
            self.processor.get_payment_status(transaction_id)

    def test_get_payment_status_empty_transaction_id(self):
        with self.assertRaises(ValueError) as context:
            self.processor.get_payment_status("")
        self.assertEqual(str(context.exception), "Transaction ID must not be empty")


if __name__ == "__main__":
    unittest.main()
