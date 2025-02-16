import requests
import base64
import logging
from django.conf import settings
from payments.models import Wallet

logger = logging.getLogger(__name__)

class MonnifyService:
    BASE_URL = settings.MONNIFY_BASE_URL
    API_KEY = settings.MONNIFY_API_KEY
    SECRET_KEY = settings.MONNIFY_SECRET_KEY
    CONTRACT_CODE = settings.MONNIFY_CONTRACT_CODE

    @classmethod
    def get_access_token(cls):
        url = f"{cls.BASE_URL}/api/v1/auth/login"
        auth_string = f"{cls.API_KEY}:{cls.SECRET_KEY}"
        auth_encoded = base64.b64encode(auth_string.encode()).decode()

        headers = {"Authorization": f"Basic {auth_encoded}", "Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers)
            response_data = response.json()
            if response.status_code == 200 and response_data.get("requestSuccessful"):
                return response_data["responseBody"].get("accessToken")
            logger.error(f"Monnify Auth Failed: {response_data}")
        except Exception as e:
            logger.error(f"Monnify Auth Error: {e}")
        return None

    @classmethod
    def create_reserved_account(cls, user):
        """Create a Monnify reserved account for the user after NIN submission."""
        wallet, _ = Wallet.objects.get_or_create(user=user)

        # ✅ Return existing account instead of creating a new one
        if wallet.virtual_account_number:
            return {"accountNumber": wallet.virtual_account_number, "bankName": wallet.bank_name}

        token = cls.get_access_token()
        if not token:
            return {"error": "Failed to authenticate with Monnify"}

        url = f"{cls.BASE_URL}/api/v1/bank-transfer/reserved-accounts"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {
            "accountReference": str(user.id),
            "accountName": f"{user.username} Wallet",
            "currencyCode": "NGN",
            "contractCode": cls.CONTRACT_CODE,
            "customerEmail": user.email,
            "customerName": user.username,
            "nin": wallet.nin,
            "getAllAvailableBanks": True,
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            logger.info(f"Monnify API Response: {response_data}")

            if response.status_code == 200 and response_data.get("requestSuccessful"):
                account_info = response_data.get("responseBody", {})
                
                logger.info(f"Monnify Returned: {account_info}")  # ✅ ADD THIS LOG

                wallet.virtual_account_number = account_info.get("accountNumber", "")
                wallet.bank_name = account_info.get("bankName", "Unknown Bank")
                # wallet.account_name = f"{user.username} Wallet"
                wallet.save()

                return {"accountNumber": wallet.virtual_account_number, "bankName": wallet.bank_name}


            logger.error(f"Monnify API Error: {response_data}")
            return {"error": response_data.get("responseMessage", "Failed to create reserved account")}

        except Exception as e:
            logger.error(f"Error creating reserved account: {e}")
            return {"error": "Failed to create reserved account"}


    # @classmethod
    # def verify_transaction(cls, transaction_reference):
    #     """Verify a Monnify transaction."""
    #     token = cls.get_access_token()
    #     if not token:
    #         return {"error": "Failed to authenticate with Monnify"}

    #     url = f"{cls.BASE_URL}/api/v1/transactions/{transaction_reference}"
    #     headers = {"Authorization": f"Bearer {token}"}

    #     try:
    #         response = requests.get(url, headers=headers)
    #         response_data = response.json()
            
    #         if response.status_code == 200 and response_data.get("requestSuccessful"):
    #             return response_data
            
    #         logger.error(f"Monnify Transaction Verification Failed: {response_data}")
    #         return {"error": "Transaction verification failed"}
    #     except Exception as e:
    #         logger.error(f"Monnify Transaction Verification Error: {e}")
    #         return {"error": "Exception occurred while verifying transaction"}