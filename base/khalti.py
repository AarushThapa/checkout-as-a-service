from django.http import HttpResponse
from django.shortcuts import redirect, render
from root import settings
import requests

live_secret_key = settings.KHALTI_LIVE_SECRET_KEY
secret_key = settings.KHALTI_LIVE_SECRET_KEY


def index(request):
    return render(template_name="index.html", request=request)


def pay_now(request):
    response = payment_initiate(amount=100, purchase_order_id=1, order_name="test")
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        payment_url = data["payment_url"]
        return redirect(payment_url)
    return HttpResponse({"error": "Error in Khalti Account."})


def verify_transaction(amount, token):
    url = settings.KHALTI_VERIFY_URL
    payload = {"token": token, "amount": amount}
    headers = {"Authorization": "Key " + secret_key}
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    else:
        return False


def payment_initiate(amount, purchase_order_id, order_name):
    return_url = f"http://127.0.0.1:8000/khalti/payment/{purchase_order_id}/success/"
    initiate_url = "https://a.khalti.com/api/v2/epayment/initiate/"
    website_url = "http://127.0.0.1:8000/"
    amount = amount * 100
    headers = {"Authorization": "Key " + secret_key}
    payload = {
        "return_url": return_url,
        "website_url": website_url,
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": order_name,
    }
    print(payload, headers)
    response = requests.post(initiate_url, headers=headers, data=payload)
    return response


def payment_success_page(request, *args, **kwargs):
    print(kwargs)
    print(request.GET.get("pk"))
    return render(template_name="khalti/payment_success.html", request=request)


def khalti_transaction_history():
    url = "https://khalti.com/api/v2/merchant-transaction"
    payload = {}
    headers = {"Authorization": "Key " + secret_key}
    response = requests.get(url, payload, headers = headers)
    return response


def khalti_transaction_detail(idx):
    url = f"https://khalti.com/api/v2/merchant-transaction/{idx}/"
    headers = {"Authorization": "Key " + secret_key}
    response = requests.get(url, headers = headers)
    return response


def khalti_transaction_status(token, amount):
    url = "https://khalti.com/api/v2/payment/status/"
    params = {
        "token": token,
        "amount": amount
        }
    headers = {"Authorization": "Key " + secret_key}
    response = requests.get(url, params, headers = headers)
    return response
