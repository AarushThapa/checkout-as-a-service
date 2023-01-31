import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

stripe.api_key = settings.STRIPE_PRIVATE_KEY


class StripePayment(View):
    def get(self, request, *args, **kwargs):
        try:
            return self.order(1, 200)
        except Exception as error:
            messages.error(self.request, str(error))
            return redirect(reverse_lazy("order_failed"))

    def order(self, order_id, amount):
        product = stripe.Product.create(name=order_id)
        amount = int(float(amount))*100
        price = stripe.Price.create(
            unit_amount=amount,
            currency="usd",
            product=product.id,
            )
        url = self.get_url()
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'{url}stripe/payment/success/?id={order_id}',
            cancel_url=f'{url}stripe/payment/failed/?id={order_id}',
        )
        return redirect(
            checkout_session.url, code=303
        )

    def get_url(self):
        scheme = self.request.is_secure() and "https" or "http"
        base_url = self.request.get_host()
        return f'{scheme}://{base_url}/'


class OrderSuccessView(TemplateView):
    template_name = "khalti/payment_success.html"


class OrderFailedView(TemplateView):
    template_name = "khalti/payment_failed.html"


class OrderPaymentSuccess(View):
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")
        print(id)
        return redirect(
            reverse_lazy("order_success")
        )


class OrderPaymentFailed(View):
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")
        print(id)
        return redirect(
            reverse_lazy("order_failed")
        )
