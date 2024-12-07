from . import Flickpay

if __name__ == "__main__":
    # secret_key = "sk-U2FsdGVkX1/e2l/P8iZygQ1vpgAcT0XXk7oCGOtZHjlm4PCoNj+CQnY23B+d09GPkqOmeXTpSplynPi8RblfdCMD6WBd2AnzYVFuLg/D6548jHqYnEsdExQgl08rZVY2"

    secret_key = "sk-U2FsdGVkX190vkQNDLz54KvLqIF6Vy9KnmjelNHw35LBp2p/0FVIEOFY3R/LVrk2me9wV++dPCPM8O3Pay1tBq9OmiCJHQgqRd6v+o9blune8AhS3oyLNRe5BIIld5GX"
    flickpay = Flickpay(secret_key)

    # Example 1: Flick Bank List SDK
    # bank_list = flickpay.flickBankListSdk()
    # print("Bank List:", bank_list)

    # Example 2: Flick Checkout SDK
    # checkout_payload = {
    #     "currency_collected": "USD",  # Example values
    #     "currency_settled": "USD",
    #     "amount": "1000",
    #     "Phoneno": "07031318231",
    #     "email": "customer@example.com",
    #     "redirectUrl": "", 
    #     "webhookUrl": "",  
    #     "transactionId": "" 
    # }

    # checkout_response = flickpay.flickCheckOut(checkout_payload)
    # print("Checkout Response:", checkout_response)
    
    # Example 3: Flick Name Inquiry SDK
    # name_payload = {
    #     "account_number": "1226910663",  
    #     "bank_code": "044"
    # }

    # name_response = flickpay.flickBankNameInquirySdk(name_payload)
    # print("Name Response:", name_response)
    
    # Example 4: Flick Intiate PayOut SDK
    # payout_payload = {
    #             "bank_name":"Access Bank",
    #             "bank_code": "044",
    #             "account_number": "1226910663",
    #             "amount":"10000",
    #             "currency":"NGN" ,
    #             "narration":"IKEMBA TEST",
    #             "beneficiary_name":"JULIUS OKAI ADEBO",
    #             "reference":"SIM+PLE0-3456789",
    #             "debit_currency":"NGN" ,
    #             "email": "kingsley@getflick.app",
    #             "mobile_number": "07031313232",
    #         }

    # payout_response = flickpay.flickInitiatePayoutSdk(payout_payload)
    # print("Payout Response:", payout_response)

    # Example 5: Flick Verify Payout SDK
    # transaction_id = "YOUR_TRANSACTION_ID_HERE"  
    # transaction_id = "SIM+PLE0-3456789"  
    # verify_response = flickpay.flickVerifyPayoutSdk(transaction_id)
    # print("Verify Payout Response:", verify_response)

    # Example 6: Flick Bvn SDK
    # bvn_payload = {
    #             "data_type":"bvn",
    #             "data": ""
    #         }

    # bvn_response = flickpay.flickIdentityBvnSdk(bvn_payload)
    # print("Payout Response:", bvn_response)
   
   
    # Example 7: Flick NIN SDK
    # nin_payload = {
    #             "nin": "",
    #             "dob": "1991-02-04"
    #         }

    # nin_response = flickpay.flickIdentityNinSdk(nin_payload)
    # print("Payout Response:", nin_response)


    # Example 8: Flick Basic CAC SDK

    # cac_payload = {
    #             "rcNumber": ""
    #         }
    # cac_response = flickpay.flickIdentityCacBasicSdk(cac_payload)
    # print("CAC Response:", cac_response)
 
    # Example 9: Flick Advance CAC SDK

    # cacAd_payload = {
    #             "rcNumber": ""
    #         }
    # cacAd_response = flickpay.flickIdentityCacBasicSdk(cacAd_payload)
    # print("CAC Response:", cacAd_response)

    # Example 10: Flick TIN SDK

    # tin_payload = {
    #             "tin": "23884159-0001"
    #         }
    # tin_response = flickpay.flickPayKybInVerification(tin_payload)
   
   
   
    # Example 11: Flick CRM SDK

    CRM_payload = {
            "amount": "10000", 
            "Phoneno": "08012345678",
            "currency_collected": "NGN",
            "currency_settled": "NGN",
            "email": "user@.com"
        }
    CRMresponse = flickpay.promptUserForDetails()
    crm_url = flickpay.flickCheckOut(CRMresponse)
    print("CRM Response:", crm_url)

#     CRMresponse = flickpay.flickCRMCheckout()
#     print(CRMresponse)
# #  flickpay = Flickpay()  # Create an instance of Flickpay
#         payment_details = self.promptUserForDetails()  # Get payment details
#         flickpay.flickCRMCheckout(payment_details)