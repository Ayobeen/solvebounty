from abc import ABC, abstractmethod

class PaymentProvider(ABC):
    @abstractmethod
    def initialize_payment(self, email: str, amount_kobo: int, reference: str, callback_url: str = None) -> dict:
        pass

    @abstractmethod
    def verify_payment(self, reference: str) -> dict:
        pass

    @abstractmethod
    def create_recipient(self, name: str, account_number: str, bank_code: str) -> dict:
        pass

    @abstractmethod
    def initiate_transfer(self, amount_kobo: int, recipient_code: str, reason: str, reference: str) -> dict:
        pass
