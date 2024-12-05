import requests
import json
import hmac
import hashlib

class PaySync():
    def __init__(self, secret_key, project_key, product_name, amount_in_cents, success_url, failed_url):
        self.server_url = "https://paysync-backend.vercel.app/pay/initiate-transaction/"
        self.secret = secret_key
        self.key = project_key
        self.product_name = product_name
        self.amount = amount_in_cents
        self.success = success_url
        self.failed = failed_url

    def initiate_payment(self, data = {}):
        print('STARTING...')
        payload = {
            "product_name": self.product_name,
            "private_key": self.key,
            "amount_in_cents": self.amount,
            "success" : self.success,
            "failed" : self.failed,
            "data" : data
        }
        print(payload)
        response = requests.post(self.server_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        response_data = response.json()

        if 'redirectUrl' in response_data:
            redirect_url = response_data['redirectUrl']
            print(redirect_url)
            redirect_url = f"https://pay-sync.vercel.app/payment-options/{redirect_url}"
            return redirect_url

        else:
            print("No redirect URL found in the response.")


def verify(secret, request):
    try:
        payload = request.get_data(as_text=True)
    except:
        pass

    payload = json.dumps(payload)

    signature = request.headers.get('X-Signature')

    computed_signature = hmac.new(
        secret.encode(),
        msg=payload.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed_signature, signature):
        print('INVALID SIGNATURE')
        return False
    
    return True
