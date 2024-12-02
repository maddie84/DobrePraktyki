from enum import Enum
import logging
from abc import ABC, abstractmethod


class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TransactionResult:
    def __init__(self, transaction_id: str, status: TransactionStatus, message: str):
        self.transaction_id = transaction_id
        self.status = status
        self.message = message


class NetworkException(Exception):
    pass


class PaymentException(Exception):
    pass


class RefundException(Exception):
    pass


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, user_id: str, amount: float) -> TransactionResult:
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> TransactionResult:
        pass

    @abstractmethod
    def getStatus(self, transaction_id: str) -> TransactionStatus:
        pass


class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
        logging.basicConfig(level=logging.INFO)

    def process_payment(self, user_id: str, amount: float) -> TransactionResult:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        if not user_id:
            raise ValueError("User ID must not be empty")

        try:
            transaction_id = self.gateway.charge(user_id, amount).transaction_id
            result = TransactionResult(
                transaction_id,
                TransactionStatus.COMPLETED,
                "Payment processed successfully",
            )
            logging.info(
                f"Payment successful: {result.transaction_id}, Amount: {amount}, User ID: {user_id}"
            )
            return result
        except Exception as e:
            logging.error(f"Payment processing failed for user {user_id}: {str(e)}")
            return TransactionResult("", TransactionStatus.FAILED, str(e))

    def refund_payment(self, transaction_id: str) -> TransactionResult:
        if not transaction_id:
            raise ValueError("Transaction ID must not be empty")

        try:
            refund_id = self.gateway.refund(transaction_id).transaction_id
            result = TransactionResult(
                refund_id, TransactionStatus.COMPLETED, "Payment refunded successfully"
            )
            logging.info(f"Refund successful: {result.transaction_id}")
            return result
        except Exception as e:
            logging.error(f"Refund failed for transaction {transaction_id}: {str(e)}")
            return TransactionResult("", TransactionStatus.FAILED, str(e))

    def get_payment_status(self, transaction_id: str) -> TransactionStatus:
        if not transaction_id:
            raise ValueError("Transaction ID must not be empty")

        try:
            status = self.gateway.getStatus(transaction_id)
            logging.info(f"Payment status for {transaction_id}: {status.name}")
            return status
        except Exception as e:
            logging.error(
                f"Failed to retrieve status for transaction {transaction_id}: {str(e)}"
            )
            raise NetworkException(str(e))
