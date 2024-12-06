from dataclasses import dataclass
from typing import Any, List, Dict, Optional
# from typing import List, Dict


@dataclass
class FlickpaySDKRequest:
    amount: str
    Phoneno: str
    currency_collected: str
    currency_settled: str
    email: str
    redirectUrl: Optional[str] = None
    webhookUrl: Optional[str] = None
    transactionId: Optional[str] = None

@dataclass
class FlickpaySDKResponse:
    statusCode: int
    status: str
    message: str
    data: List[Dict[str, str]]

    def __str__(self):
        return f"StatusCode: {self.statusCode}\nStatus: {self.status}\nMessage: {self.message}\nData: {self.data}"

@dataclass
class FlickBankListResponse:
    status: int
    message: str
    data: List[Dict[str, str]]

    def __str__(self):
        return f"Status: {self.status}\nMessage: {self.message}\nData: {self.data}."


@dataclass
class Bank:
    status: int
    message: str
    form: str
    data: List[Dict[str, str]]

    def __str__(self):
        return f"Status: {self.status}\nMessage: {self.message}\nData: {self.data}."


# class Bank:
#     def __init__(self, logo: str, slug: str, bank_code: str, country: str, active: bool, bank_name: str):
#         self.logo = logo
#         self.slug = slug
#         self.bank_code = bank_code
#         self.country = country
#         self.active = active
#         self.bank_name = bank_name


# class FlickBankListResponse:
#     def __init__(self, status: int, message: str, data: List[Dict[str, Any]]):
#         self.status = status
#         self.message = message
#         self.data = data


class FlickBankNameResponse:
    status: int
    message: str
    account_number: str
    account_name: str


class FlickPayoutResponse:
    def __init__(self, status: int, Id: str, message: str, description: str):
        self.status = status
        self.Id = Id
        self.message = message
        self.description = description


class FlickVerifyPayoutResponse:
    def __init__(self, status: int, Id: str, account_number: str, account_name: str, bank_name: str,
                 amount: str, currency: str, transaction_status: str):
        self.status = status
        self.Id = Id
        self.account_number = account_number
        self.account_name = account_name
        self.bank_name = bank_name
        self.amount = amount
        self.currency = currency
        self.transaction_status = transaction_status


class FlickBvnResponse:
    def __init__(self, status: int, message: str, data: Any):
        self.status = status
        self.message = message
        self.data = data


class FlickCacResponse:
    def __init__(self, status: int, message: str, data: Any):
        self.status = status
        self.message = message
        self.data = data


class FlickNinResponse:
    def __init__(self, status: int, message: str, data: Any):
        self.status = status
        self.message = message
        self.data = data
