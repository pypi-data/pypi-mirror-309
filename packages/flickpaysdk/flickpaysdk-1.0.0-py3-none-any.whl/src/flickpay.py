import requests 
from .types import (
        FlickBankListResponse,
        FlickBankNameResponse,
        FlickPayoutResponse,
        FlickVerifyPayoutResponse,
        FlickBvnResponse,
        FlickCacResponse,
        FlickNinResponse,
        FlickpaySDKRequest,
        FlickpaySDKResponse,
        FlickBankNameSdkRequest,
        FlickPayoutSdkRequest,
        FlickBvnRequest,
        FlickNinRequest,
        FlickCacRequest,
        FlickTinRequest,
        FlickTinResponse,
    )
from typing import Dict, Any


class Flickpay:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def flickCheckOut(self, request: FlickpaySDKRequest) -> FlickpaySDKResponse:
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

    def flickBankListSdk(self) -> FlickBankListResponse:
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

    def flickBankNameInquirySdk(self, request:FlickBankNameSdkRequest ) -> FlickBankNameResponse:
        try:
            payload = {
                "account_number": request.get("account_number"),
                "bank_code": request.get("bank_code")
            }
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
        except requests.exceptions.HTTPError as http_err:
        
            try:
                error_details = response.json()  
            except ValueError: 
                error_details = response.json()

            return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}


    def flickInitiatePayoutSdk(self, request:FlickPayoutSdkRequest) -> FlickPayoutResponse:
        try:
            payload = {
                "bank_name": request.get("bank_name"),
                "bank_code": request.get("bank_code"),
                "account_number": request.get("account_number"),
                "amount": request.get("amount"),
                "currency": request.get("currency"),
                "narration": request.get("narration"),
                "beneficiary_name": request.get("beneficiary_name"),
                "reference": request.get("reference"),
                "debit_currency": request.get("debit_currency"),
                "email": request.get("email"),
                "mobile_number": request.get("mobile_number"),
            }
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
        except requests.exceptions.HTTPError as http_err:
        
            try:
                error_details = response.json()  
            except ValueError: 
                error_details = response.json()

            return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def flickVerifyPayoutSdk(self, transaction_id: str) -> FlickVerifyPayoutResponse:
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
        except requests.exceptions.HTTPError as http_err:
        
            try:
                error_details = response.json()  
            except ValueError: 
                error_details = response.json()

            return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def flickIdentityBvnSdk(self, request:FlickBvnRequest) -> FlickBvnResponse:
        try:
            payload = {
                "data_type": request.get("data_type"),
                "data": request.get("data"),
            }
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"https://flickopenapi.co/kyc/identity-bvn",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickBvnResponse(
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

    
    def flickIdentityNinSdk(self, request:FlickNinRequest) -> FlickNinResponse:
        try:
            payload = {
                "nin": request.get("nin"),
                "dob": request.get("dob")
            }
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"https://flickopenapi.co/kyc/identity-nin",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            if response.headers.get("Content-Type", "").startswith("application/json"):

                print('here............')
                data = response.json()
                return FlickNinResponse(
                status=data["status"], message=data["message"], data=data["data"]
                )
            else:
                return {
                "success": False,
                "error": "Unexpected response format",
                "raw_response": response.text
                }
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out. Please try again later."}

        except requests.exceptions.ConnectionError:
        
            return {"success": False, "error": "Network problem. Could not connect to server."}

        except requests.exceptions.HTTPError as http_err:
            if http_err.response is not None:

        
                try:
                    error_details = http_err.response.json()  
                except ValueError: 
                    error_details = http_err.response.text
                    
                return {
                "success": False,
                "error": "HTTP error occurred.",
                "status_code": http_err.response.status_code,
                "details": error_details
            }
            else:

                return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}
        except requests.exceptions.RequestException as req_err:
    
            return {"success": False, "error": f"Request error: {req_err}"}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def flickIdentityCacBasicSdk(self, request:FlickCacRequest) -> FlickCacResponse:
        try:
            payload = {
                "rcNumber": request.get("rcNumber")
            }
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"https://flickopenapi.co/kyb/biz-basic",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            if response.headers.get("Content-Type", "").startswith("application/json"):

                print('here............')
                data = response.json()
                return FlickCacResponse(
                status=data["status"], message=data["message"], data=data["data"]
                )
            else:
                return {
                "success": False,
                "error": "Unexpected response format",
                "raw_response": response.text
                }
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out. Please try again later."}

        except requests.exceptions.ConnectionError:
        
            return {"success": False, "error": "Network problem. Could not connect to server."}

        except requests.exceptions.HTTPError as http_err:
            if http_err.response is not None:

        
                try:
                    error_details = http_err.response.json()  
                except ValueError: 
                    error_details = http_err.response.text
                    
                return {
                "success": False,
                "error": "HTTP error occurred.",
                "status_code": http_err.response.status_code,
                "details": error_details
            }
            else:

                return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}
        except requests.exceptions.RequestException as req_err:
    
            return {"success": False, "error": f"Request error: {req_err}"}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
 
   
    def flickIdentityCacAdvanceSdk(self, request:FlickCacRequest) -> FlickCacResponse:
        try:
            payload = {
                "rcNumber": request.get("rcNumber")
            }
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"https://flickopenapi.co/kyb/biz-advance",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            if response.headers.get("Content-Type", "").startswith("application/json"):

                print('here............')
                data = response.json()
                return FlickCacResponse(
                status=data["status"], message=data["message"], data=data["data"]
                )
            else:
                return {
                "success": False,
                "error": "Unexpected response format",
                "raw_response": response.text
                }
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out. Please try again later."}

        except requests.exceptions.ConnectionError:
        
            return {"success": False, "error": "Network problem. Could not connect to server."}

        except requests.exceptions.HTTPError as http_err:
            if http_err.response is not None:

        
                try:
                    error_details = http_err.response.json()  
                except ValueError: 
                    error_details = http_err.response.text
                    
                return {
                "success": False,
                "error": "HTTP error occurred.",
                "status_code": http_err.response.status_code,
                "details": error_details
            }
            else:

                return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}
        except requests.exceptions.RequestException as req_err:
    
            return {"success": False, "error": f"Request error: {req_err}"}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
 
    
    def flickPayKybInVerification(self, request:FlickTinRequest) -> FlickTinResponse:
        try:
            payload = {
                "tin": request.get("tin")
            }
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"https://flickopenapi.co/kyb/tin-verification",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            if response.headers.get("Content-Type", "").startswith("application/json"):

                print('here............')
                data = response.json()
                return FlickTinResponse(
                status=data["status"], message=data["message"], data=data["data"]
                )
            else:
                return {
                "success": False,
                "error": "Unexpected response format",
                "raw_response": response.text
                }
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out. Please try again later."}

        except requests.exceptions.ConnectionError:
        
            return {"success": False, "error": "Network problem. Could not connect to server."}

        except requests.exceptions.HTTPError as http_err:
            if http_err.response is not None:

        
                try:
                    error_details = http_err.response.json()  
                except ValueError: 
                    error_details = http_err.response.text
                    
                return {
                "success": False,
                "error": "HTTP error occurred.",
                "status_code": http_err.response.status_code,
                "details": error_details
            }
            else:

                return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}
        except requests.exceptions.RequestException as req_err:
    
            return {"success": False, "error": f"Request error: {req_err}"}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
 
   
    def promptUserForDetails(self):
      
        print("Enter payment details:")
        amount = input("Amount: ")
        phone_number = input("Phone Number: ")
        currency_collected = input("Currency (e.g., NGN): ")
        email = input("Email: ")
        return {
            "amount": amount,
            "Phoneno": phone_number,
            "currency_collected": currency_collected,
            "currency_settled": "NGN", 
            "email": email,
        }

    def flickCRMCheckout(self, promptUserForDetails):
        
        request_data = self.promptUserForDetails()

        try:
          
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.secret_key}",
            }
            url = "https://flickopenapi.co/collection/create-charge"
            
       
            response = requests.post(url, json=request_data, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP errors
            
            # Process the JSON response
            if response.status_code == 200:
                data = response.json()
                redirect_url = data.get("data", {}).get("url")
            
                if redirect_url:
                # Simulate redirect if the environment was a browser
                    print(f"Redirecting to: {redirect_url}")
                return {"success": True, "redirect_url": redirect_url}
                if isinstance(data.get("data"), dict) and data["data"].get("url"):
                    print(f"Redirect URL: {data['data']['url']}")
                    return data['data']
                else:
                    return {"success": False, "error": "Unexpected response format", "data": data}
            
            else:
                return {"success": False, "error": f"Failed with status code {response.status_code}", "data": response.json()}

        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out. Please try again later."}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Network problem. Could not connect to the server."}
        except requests.exceptions.HTTPError as http_err:
            return {"success": False, "error": f"HTTP error occurred: {http_err}", "status_code": response.status_code}
        except requests.exceptions.RequestException as req_err:
            return {"success": False, "error": f"Request failed: {str(req_err)}"}
        except requests.exceptions.RequestException as req_err:
            return {"success": False, "error": f"Request error: {req_err}"}