import requests 
from .types  import (
    FlickBankListResponse, FlickBankNameResponse, FlickPayoutResponse,
    FlickVerifyPayoutResponse, FlickBvnResponse, FlickCacResponse, FlickNinResponse, FlickpaySDKRequest, FlickpaySDKResponse,
)
from typing import Dict, Any


class Flickpay:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def flick_check_out(self, request: FlickpaySDKRequest) -> FlickpaySDKResponse:
        try:
            payload = {
                "amount": request.get("amount"),
                "Phoneno": request.get("Phoneno"),
                "currency_collected": request.get("currency_collected"),
                "currency_settled": request.get("currency_settled"),
                "email": request.get("email"),
                "redirectUrl": request.get("redirectUrl"),
                "webhookUrl": request.get("webhookUrl")
            }    
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url="https://flickopenapi.co/collection/create-charge",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickpaySDKResponse(
                statusCode=data["statusCode"], status=data["status"], message=data["message"], data=data["data"]
            )
        except requests.exceptions.HTTPError as http_err:
        
            try:
                error_details = response.json()  
            except ValueError: 
                error_details = response.json()

            return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def flick_bank_list_sdk(self) -> FlickBankListResponse:
        try:
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.get(
                url="https://flickopenapi.co/merchant/banks",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickBankListResponse(
                status=data["status"], message=data["message"], data=data["data"]
            )
        
        except requests.exceptions.HTTPError as http_err:
        
            try:
                error_details = response.json()  
            except ValueError: 
                error_details = response.json()

            return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def flick_bank_name_inquiry_sdk(self, payload: Dict[str, str]) -> FlickBankNameResponse:
        try:
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url="https://flickopenapi.co/merchant/name-enquiry",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickBankNameResponse(
                status=data["status"], message=data["message"],
                account_number=data["data"]["account_number"], account_name=data["data"]["account_name"]
            )
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def flick_initiate_payout_sdk(self, payload: Dict[str, Any]) -> FlickPayoutResponse:
        try:
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url="https://flickopenapi.co/transfer/payout",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickPayoutResponse(
                status=data["status"], Id=data["Id"], message=data["message"], description=data["description"]
            )
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def flick_verify_payout_sdk(self, transaction_id: str) -> FlickVerifyPayoutResponse:
        try:
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.get(
                url=f"https://flickopenapi.co/transfer/verify/{transaction_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickVerifyPayoutResponse(
                status=data["status"], Id=data["Id"], account_number=data["account_number"],
                account_name=data["account_name"], bank_name=data["bank_name"], amount=data["amount"],
                currency=data["currency"], transaction_status=data["transaction_status"]
            )
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def flick_identity_bvn_sdk(self, transaction_id: str) -> FlickVerifyPayoutResponse:
        try:
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.get(
                url=f"https://flickopenapi.co/transfer/verify/{transaction_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickVerifyPayoutResponse(
                status=data["status"], Id=data["Id"], account_number=data["account_number"],
                account_name=data["account_name"], bank_name=data["bank_name"], amount=data["amount"],
                currency=data["currency"], transaction_status=data["transaction_status"]
            )
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def flick_identity_nin_sdk(self, transaction_id: str) -> FlickVerifyPayoutResponse:
        try:
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.get(
                url=f"https://flickopenapi.co/transfer/verify/{transaction_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickVerifyPayoutResponse(
                status=data["status"], Id=data["Id"], account_number=data["account_number"],
                account_name=data["account_name"], bank_name=data["bank_name"], amount=data["amount"],
                currency=data["currency"], transaction_status=data["transaction_status"]
            )
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def flick_identity_cac_basic_sdk(self, transaction_id: str) -> FlickVerifyPayoutResponse:
        try:
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.get(
                url=f"https://flickopenapi.co/transfer/verify/{transaction_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickVerifyPayoutResponse(
                status=data["status"], Id=data["Id"], account_number=data["account_number"],
                account_name=data["account_name"], bank_name=data["bank_name"], amount=data["amount"],
                currency=data["currency"], transaction_status=data["transaction_status"]
            )
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
   
    def flick_identity_cac_advance_sdk(self, transaction_id: str) -> FlickVerifyPayoutResponse:
        try:
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.get(
                url=f"https://flickopenapi.co/transfer/verify/{transaction_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickVerifyPayoutResponse(
                status=data["status"], Id=data["Id"], account_number=data["account_number"],
                account_name=data["account_name"], bank_name=data["bank_name"], amount=data["amount"],
                currency=data["currency"], transaction_status=data["transaction_status"]
            )
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def flick_pay_kyb_in_verification(self, transaction_id: str) -> FlickVerifyPayoutResponse:
        try:
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.get(
                url=f"https://flickopenapi.co/transfer/verify/{transaction_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickVerifyPayoutResponse(
                status=data["status"], Id=data["Id"], account_number=data["account_number"],
                account_name=data["account_name"], bank_name=data["bank_name"], amount=data["amount"],
                currency=data["currency"], transaction_status=data["transaction_status"]
            )
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def flick_crm_check_out(self, transaction_id: str) -> FlickVerifyPayoutResponse:
        try:
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.get(
                url=f"https://flickopenapi.co/transfer/verify/{transaction_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickVerifyPayoutResponse(
                status=data["status"], Id=data["Id"], account_number=data["account_number"],
                account_name=data["account_name"], bank_name=data["bank_name"], amount=data["amount"],
                currency=data["currency"], transaction_status=data["transaction_status"]
            )
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    