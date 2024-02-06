import stripe
import json

from django.http import JsonResponse
from django.shortcuts import  render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Food

endpoint_secret = 'whsec_c1913c50279be0efc5735f4989769d58dbfc4ef3971b244ff61524c9b208e15b'


secret_key = "sk_test_51OZTUEBFkLqjc7QTFXwxu3Me4oCgklY5DLs5jqAUEkYky5e4VBfyAE5FHpp99Kc8RUqOlxvoHGDRtDHOJAnhFvGJ00YkqrxM0U"

stripe.api_key = secret_key

@method_decorator(csrf_exempt, name='dispatch')
class Products(View):

    def get(self, request, *args, **kwargs):
        return render(request, "products.html", context={
            "items": Food.objects.all()
        })
    
@method_decorator(csrf_exempt, name='dispatch')
class Success(View):

    def get(self, request, *args, **kwargs):
        # payment_intent=pi_3OeofKBFkLqjc7QT0mAum9s8
        # payment_intent_client_secret=pi_3OeofKBFkLqjc7QT0mAum9s8_secret_t7KAbPpqPsl3cQCaHKjN207i0
        # redirect_status=succeeded
        return render(request, "success.html", context={})
@method_decorator(csrf_exempt, name='dispatch')
class Cancel(View):

    def get(self, request, *args, **kwargs):
        # payment_intent=pi_3OeofKBFkLqjc7QT0mAum9s8
        # payment_intent_client_secret=pi_3OeofKBFkLqjc7QT0mAum9s8_secret_t7KAbPpqPsl3cQCaHKjN207i0
        # redirect_status=succeeded
        return render(request, "cancel.html", context={})

@method_decorator(csrf_exempt, name='dispatch')
class Buy(View):
    def post(self, request, product_name: str, *args, **kwargs):

        food = Food.objects.get(name=product_name)

        intent = stripe.PaymentIntent.create(
            # 價格
            amount=50000, 
            currency='usd',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )
        

        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    

@method_decorator(csrf_exempt, name='dispatch')
class Subscription(View):
    def get(self, request, product_name: str, *args, **kwargs):

        food = Food.objects.get(name=product_name)

        return render(request, "sub.html", context={
            "product": food,
        })
    
    def post(self, request, product_name: str, *args, **kwargs): 

        data = json.loads(request.body)
        prices = stripe.Price.list(
            lookup_keys=[data["lookup_key"]],
            expand=["data.product"]
        )


        DOMAIN = "http://127.0.0.1:8000"

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': prices.data[0].id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            subscription_data={
                "trial_period_days": 2
            },
            success_url=f"{DOMAIN}/shop/success" + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url= f"{DOMAIN}/shop/cancel",
        )

        return JsonResponse({
            "redirect": checkout_session.url
        })

@method_decorator(csrf_exempt, name='dispatch')
class Webhook(View):

    def post(self, request, *args, **kwargs):
        event = None
        payload = request.body
        sig_header = request.headers['STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e


        print(f"處理 {event['type']} 事件中...!")
        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
          payment_intent = event['data']['object']
        # ... handle other event types
        # else:
        #     print('Unhandled event type {}'.format(event['type']))

        return JsonResponse({
            "success": True
        })




# 每次更改訂閱紀錄的模擬時間時
# 處理 test_helpers.test_clock.advancing 事件中...!
# [05/Feb/2024 05:36:34] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 payment_intent.succeeded 事件中...!
# [05/Feb/2024 05:36:38] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 charge.succeeded 事件中...!
# [05/Feb/2024 05:36:38] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 customer.updated 事件中...!
# [05/Feb/2024 05:36:38] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 payment_intent.created 事件中...!
# [05/Feb/2024 05:36:38] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 invoice.updated 事件中...!
# [05/Feb/2024 05:36:39] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 invoice.paid 事件中...!
# [05/Feb/2024 05:36:39] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 invoice.payment_succeeded 事件中...!
# [05/Feb/2024 05:36:39] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 invoice.finalized 事件中...!
# [05/Feb/2024 05:36:39] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 invoice.created 事件中...!
# [05/Feb/2024 05:36:40] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 customer.subscription.updated 事件中...!
# [05/Feb/2024 05:36:40] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 test_helpers.test_clock.ready 事件中...!
# [05/Feb/2024 05:36:41] "POST /shop/webhook HTTP/1.1" 200 17




# 每日更新 但是訂閱並沒有超過 Trial Date
# 處理 customer.updated 事件中...!
# [05/Feb/2024 05:57:15] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 test_helpers.test_clock.created 事件中...!
# [05/Feb/2024 05:57:15] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 test_helpers.test_clock.ready 事件中...!
# [05/Feb/2024 05:57:16] "POST /shop/webhook HTTP/1.1" 200 17


# 每次更動時間會觸發
# 處理 test_helpers.test_clock.advancing 事件中...!
# [05/Feb/2024 05:59:30] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 test_helpers.test_clock.ready 事件中...!
# [05/Feb/2024 05:59:32] "POST /shop/webhook HTTP/1.1" 200 17
    

# 剛好超過購買時間 並且 需要開始付費購買了
# 處理 test_helpers.test_clock.advancing 事件中...!
# [05/Feb/2024 06:01:37] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 invoice.created 事件中...!
# [05/Feb/2024 06:01:39] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 customer.subscription.updated 事件中...!
# [05/Feb/2024 06:01:39] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 test_helpers.test_clock.ready 事件中...!
# [05/Feb/2024 06:01:40] "POST /shop/webhook HTTP/1.1" 200 17
    

# 到了隔天 付費
# 處理 test_helpers.test_clock.advancing 事件中...!
# [05/Feb/2024 06:04:41] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 payment_intent.succeeded 事件中...!
# [05/Feb/2024 06:04:44] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 charge.succeeded 事件中...!
# [05/Feb/2024 06:04:44] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 customer.updated 事件中...!
# [05/Feb/2024 06:04:45] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 payment_intent.created 事件中...!
# [05/Feb/2024 06:04:45] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 invoice.updated 事件中...!
# [05/Feb/2024 06:04:45] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 invoice.paid 事件中...!
# [05/Feb/2024 06:04:45] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 invoice.payment_succeeded 事件中...!
# [05/Feb/2024 06:04:45] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 invoice.finalized 事件中...!
# [05/Feb/2024 06:04:45] "POST /shop/webhook HTTP/1.1" 200 17
# 處理 test_helpers.test_clock.ready 事件中...!
# [05/Feb/2024 06:04:46] "POST /shop/webhook HTTP/1.1" 200 17