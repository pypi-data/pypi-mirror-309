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
class Bank:
    status: int
    message: str
    form: str
    data: List[Dict[str, str]]


@dataclass
class FlickBankListResponse:
    status: int
    message: str
    data: List[Bank]

    def __str__(self):
        return f"Status: {self.status}\nMessage: {self.message}\nData: {self.data}."



@dataclass
class FlickBankNameSdkRequest:
    account_number: str
    bank_code: str



@dataclass
class FlickBankNameData:
    account_number: str
    account_name: str


@dataclass
class FlickBankNameResponse:
    status: int
    message: str
    account_number: str
    account_name: str

    def __str__(self):
        return f"Status: {self.status}\nMessage: {self.message}\nAccount Number: {self.account_number}\nAccount Name: {self.account_name}"



@dataclass
class FlickPayoutSdkRequest:
    bank_name: str
    bank_code: str
    account_number: str
    amount: str
    narration: str
    currency: str
    beneficiary_name: str
    reference: str
    debit_currency: str
    email: str
    mobile_number: str

@dataclass
class FlickPayoutResponse:
    status: int
    Id: str
    message: str
    description: str

    def __str__(self):
        return f"Status: {self.status}\nID: {self.Id}\nMessage: {self.message}\nDescription: {self.description}"

@dataclass
class FlickVerifyPayoutResponse:
    status: int
    Id: str
    account_number: str
    account_name: str
    bank_name: str
    amount: str
    currency: str
    transaction_status: str

    def __str__(self):
        return f"Status={self.status}\nID={self.Id}\nAccount_number={self.account_number}\nAccount_name={self.account_name}\nBank_name={self.bank_name}\nAmount={self.amount}\nCurrency={self.currency}\nTransaction_status={self.transaction_status}"


@dataclass
class FlickBvnRequest:
    secret_key: str
    data_type: str
    data: str

@dataclass
class FlickBvnResponse:
    status: int
    message: str
    data: Any 

    def __str__(self):
        return f"Status={self.status}\nMessage={self.message}\nData={self.data}"



@dataclass
class FlickNinRequest:
    nin: str
    dob: str

@dataclass
class FlickNinResponse:
    status: int
    message: str
    data: Any  # will be adjusted later

    def __str__(self):
        return f"Status={self.status}\nMessage={self.message}\nData={self.data}"



@dataclass
class FlickCacRequest:
    rcNumber: str


@dataclass
class FlickCacResponse:
    status: int
    message: str
    data: Any

    def __str__(self):
        return f"Status={self.status}\nMessage={self.message}\nData={self.data}"


@dataclass
class FlickTinRequest:
    tin: str


@dataclass
class FlickTinResponse:
    status: int
    message: str
    data: Any  

    def __str__(self):
        return f"Status={self.status}\nMessage={self.message}\nData={self.data}"
