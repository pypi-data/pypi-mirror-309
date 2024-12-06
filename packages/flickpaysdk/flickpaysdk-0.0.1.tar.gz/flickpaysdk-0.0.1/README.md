# FlickPaySDK for ```python

FlickPaySDK is a secure and quick way for customers to access accounts and interact with the Flick API for Identity, Financial Data, Payouts, Collections, and Miscellaneous operations. It provides a straightforward integration for ```python developers.

## Features
- **Checkout:** Collect payments easily with various options.
- **Banking:** Retrieve bank lists, perform name inquiries, and manage payouts.
- **Identity Verification:** Verify BVN, NIN, CAC, and more.
- **Secure SDK:** Handles multi-factor authentication, credential validation, and error handling.

---

## Getting Started

1. **Register on Flick:**
   Sign up at [Flick](https://login.merchant.getflick.co/getstarted) to obtain your API keys (`secret_key` and `public_key`).

2. **Installation:**
   Install the package via `pip`:

   ```bash
   pip install flickpaysdk

Initialization: Create an instance of the FlickPay class using your secret_key.

Usage
Initialize the SDK
```python
Copy code
from flickpaysdk import Flickpay

# Replace with your actual secret key
secret_key = "your_secret_key"
flickpay = Flickpay(secret_key)
Checkout
Initiate a checkout process:
```
```python
Copy code
checkout_payload = {
    "amount": "1000",
    "Phoneno": "1234567890",
    "currency_collected": "NGN",
    "currency_settled": "USD",
    "email": "example@example.com",
    "redirectUrl": "https://example.com/redirect",
    "webhookUrl": "https://example.com/webhook",
}
response = flickpay.flick_check_out(checkout_payload)
print(response)
Bank List Retrieval
Retrieve a list of supported banks:
```
```python
Copy code
response = flickpay.flick_bank_list_sdk()
print(response)
Bank Name Inquiry
Perform a bank name inquiry:
```
```python
Copy code
bank_name_payload = {
    "account_number": "1234567890",
    "bank_code": "001"
}
response = flickpay.flick_bank_name_inquiry_sdk(bank_name_payload)
print(response)
```
Payout Initialization
Initiate a payout:

```python
Copy code
payout_payload = {
    "bank_name": "Example Bank",
    "bank_code": "012",
    "account_number": "1234567890",
    "amount": "1000",
    "narration": "Payment for services",
    "currency": "NGN",
    "beneficiary_name": "John Doe",
}
response = flickpay.flick_initiate_payout_sdk(payout_payload)
print(response)
```
Payout Verification
Verify a payout:

```python
Copy code
transaction_id = "1234567890"
response = flickpay.flick_verify_payout_sdk(transaction_id)
print(response)
```
Identity Verification
Perform various identity verifications:

```python
Copy code
# BVN Verification
response = flickpay.flick_identity_bvn_sdk({"bvn": "12345678901"})
print(response)

# NIN Verification
response = flickpay.flick_identity_nin_sdk({"nin": "12345678901"})
print(response)

# CAC Verification (Basic)
response = flickpay.flick_identity_cac_basic_sdk({"rc_number": "123456"})
print(response)
Best Practices
Always handle exceptions raised by API calls.
Store your secret_key securely to prevent unauthorized access.
Support
If you need help with FlickPaySDK or your Flick integration, reach out to support@getflick.app or join our Slack channel.

License
This project is licensed under the MIT License.