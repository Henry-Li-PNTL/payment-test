
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import Webhook, Products, Buy, Success, Cancel, Subscription, AttachPaymentMethod

urlpatterns = [
    path("webhook", Webhook.as_view()),
    path("success", Success.as_view()),
    path("cancel", Cancel.as_view()),
    path("products/<str:product_name>", Buy.as_view()),
    path("products", Products.as_view()),
    path("subscription/<str:product_name>", Subscription.as_view()),
    path("attach", AttachPaymentMethod.as_view()),
]
