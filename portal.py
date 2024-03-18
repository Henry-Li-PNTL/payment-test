import random
import stripe
import datetime
import sys


# 公司的
stripe.api_key = "sk_test_51OOxrkHUX1GxVLtdNFSqrQiwofWKURdHOAYi9zoldTwit7Js4uUJpnWVR0TwVYCy4ubr9slddAneNrPp7BDerm2W00D2pMsRq2"


# Switch
# stripe.api_key = "sk_test_51OZTUEBFkLqjc7QTFXwxu3Me4oCgklY5DLs5jqAUEkYky5e4VBfyAE5FHpp99Kc8RUqOlxvoHGDRtDHOJAnhFvGJ00YkqrxM0U"





configuration_id = "bpc_1OqQJtHUX1GxVLtdjT8tPISn"


x = None
if sys.argv[2] == "y":
    x = stripe.billing_portal.Configuration.create(
    business_profile={
        "headline": "RAPD",
    },
    features={
        "customer_update": {
            "allowed_updates": ["email", "tax_id", "address", "phone"], 
            "enabled": True
        },
        "payment_method_update": {
            "enabled": True
        },
        "subscription_cancel": {
            "enabled": True,
            "mode": "at_period_end",
            "cancellation_reason": {
                "enabled": True,
                "options": [ "customer_service", "low_quality", "missing_features", "other", "switched_service", "too_complex", "too_expensive", "unused",]
            }
        },
        "subscription_update": {
            "default_allowed_updates": ["price"],
            "enabled": True,
            "products": [
                {
                    # 公司的
                    "prices": ["price_1OpKixHUX1GxVLtdA9UXqpHN", "price_1Op64XHUX1GxVLtd1mLWdsxw"],
                    "product": "prod_PeOsPAwnsEuhyo"

                    # 我的
                    # "prices": ["price_1OkMyxBFkLqjc7QTSUA15pIY", "price_1OetlBBFkLqjc7QTKBD9TDFO"],
                    # "product": "prod_PTrUBPTEJuplWc"
                }
            ]
        },
        "invoice_history": {
            "enabled": True
        },
    },
    )

    print(x.stripe_id)
    configuration_id = x.stripe_id


eric = "cus_PfnCRyNxwsJvYQ"
me = "cus_PZV6GO3wuec92B"
xxx = stripe.billing_portal.Session.create(
  customer=eric,
  configuration=configuration_id,
  return_url="https://example.com/account",
)
print(xxx["url"])