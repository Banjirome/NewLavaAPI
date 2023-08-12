import hmac
import json
import hashlib
import requests
import random
import time



class Payment():
    def __init__(self, api_token, shop_id, orderID, paymentID, payment_url):
        self.api_token = api_token
        self.shop_id = shop_id
        self.orderID = orderID
        self.headers = {}
        self.paymentID = paymentID
        self.api_url = "https://api.lava.ru"
        self.url = payment_url

    def signer_func(self, data):
        jsonStr = json.dumps(data).encode()

        sign = hmac.new(bytes(self.api_token, 'UTF-8'), jsonStr, hashlib.sha256).hexdigest()
        return sign
    
    def check_invoice_status(self):
        data = {
            "shopId": self.shop_id,
            "orderId": self.orderID,
            "invoiceId": self.paymentID
        }
        headers = self.headers
        headers["Signature"] = self.signer_func(data)

        resp = requests.post(f"{self.api_url}/business/invoice/status", json=data, headers=headers).json()
        if resp['data']['status'] == "success":
            return True
        else:
            return False


class NewLavaAPI():
    def __init__(self, api_token: str, shop_id: str):
        self.api_token = api_token
        self.shop_id = shop_id
        self.headers = {}
        self.url = "https://api.lava.ru"
        self.auth_test()



    class CreateInvoiceError(Exception):
        pass

    class AuthError(Exception):
        pass

    def signer_func(self, data):
        jsonStr = json.dumps(data).encode()

        sign = hmac.new(bytes(self.api_token, 'UTF-8'), jsonStr, hashlib.sha256).hexdigest()
        return sign

    def auth_test(self):
        data = {
            "shopId": self.shop_id
        }
        headers = self.headers
        headers["Signature"] = self.signer_func(data)
        resp = requests.post(f'{self.url}/business/shop/get-balance', json=data, headers=headers).json()
        try:
            if resp['status_check']:
                return True
            else:
                raise self.AuthError("Invalid token or shop")
        except:
            raise self.AuthError("Invalid token or shop")

    def create_invoice(self, orderId: int, sum: float, comment: str):
        data = {
            "shopId": self.shop_id,
            "orderId": orderId,
            "sum": sum,
            "comment": comment
        }

        headers = self.headers
        headers['Signature'] = self.signer_func(data)

        resp = requests.post(f"{self.url}/business/invoice/create", json=data, headers=headers).json()
        try:
            if resp['status_check']:
                return Payment(self.api_token, self.shop_id, orderId, resp['data']['id'], resp['data']['url'])
            else:
                raise self.CreateInvoiceError("Error occured when tryed to create invoice")
        except:
            raise self.CreateInvoiceError("Error occured when tryed to create invoice")
    
    def balance(self) -> float:
        data = {
            "shopId": self.shop_id
        }
        headers = self.headers
        headers['Signature'] = self.signer_func(data)
        resp = requests.post(f"{self.url}/business/shop/get-balance", json = data, headers=headers).json()
        return resp['data']['balance']
        