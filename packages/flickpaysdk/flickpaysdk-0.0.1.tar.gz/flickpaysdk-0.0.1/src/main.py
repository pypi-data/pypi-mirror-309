from .sdk import Flickpay

if __name__ == "__main__":
    secret_key = "sk-U2FsdGVkX1/i+YmuT/sNUaWenD/ZCUWD32NavuXRzS9h3Mqb2vJixlZqVvvwdRNutWSuWTHlzTHBsVgx2YA6GVoLCmePC0FH1VNHRHDp9OydGDxdgMy4YsHM+9u7pBhp"
    flickpay = Flickpay(secret_key)

    # Example 1: Flick Bank List SDK
    bank_list = flickpay.flick_bank_list_sdk()
    print("Bank List:", bank_list)

    # # Example 2: Flick Bank Name Inquiry
    # bank_name_payload = {"account_number": "1234567890", "bank_code": "001"}
    # bank_name = flickpay.flick_bank_name_inquiry_sdk(bank_name_payload)
    # print("Bank Name Inquiry:", bank_name)

    # Example 3: Flick Checkout SDK
    checkout_payload = {
        "currency_collected": "USD",  # Example values
        "currency_settled": "USD",
        "amount": "1000",
        "Phoneno": "07031318231",
        "email": "customer@example.com",
        "redirectUrl": "",  # Optional
        "webhookUrl": "",   # Optional
        "transactionId": ""  # Optional
    }

    checkout_response = flickpay.flick_check_out(checkout_payload)
    print("Checkout Response:", checkout_response)
