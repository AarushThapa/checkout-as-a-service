from django.urls import path
from .khalti import payment_success_page, index, pay_now
from .stripe import StripePayment, OrderSuccessView, OrderFailedView, OrderPaymentSuccess, OrderPaymentFailed

urlpatterns = [
    path("", index, name="index"), 
    path("pay/", pay_now, name="khalti_payment"), 
    path("khalti/payment/<int:pk>/success/", payment_success_page, name="payment_success_page")
]

urlpatterns += [
    path("stripe/pay/", StripePayment.as_view(), name="stripe_payment"),
    path("stripe/success/", OrderSuccessView.as_view(), name="order_success"),
    path("stripe/payment/success/", OrderPaymentSuccess.as_view(), name="order_payment_success"),
    path("stripe/payment/failed/", OrderPaymentFailed.as_view(), name="order_payment_failed"),
    path("stripe/failed/", OrderFailedView.as_view(), name="order_failed"),
]