import stripe
import json
import datetime
import random

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



def get_next_month_timestamp(next_day: int) -> int: 
    ## 當前日期
    now = datetime.datetime.now()

    # 如果當前日期已經超過這個月的15號，則找下個月的15號
    if now.day > next_day:
        # 下個月的年份和月份
        next_month_year = now.year + (1 if now.month == 12 else 0)
        next_month = 1 if now.month == 12 else now.month + 1

        # 下個月的15號
        next_15th = datetime.datetime(next_month_year, next_month, next_day)
    else:
        # 這個月的15號
        next_15th = datetime.datetime(now.year, now.month, next_day)

    # 轉換為timestamp int
    next_15th_timestamp = int(next_15th.timestamp())
    return next_15th_timestamp

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



        milk_every_day_10usd = "price_1OetlBBFkLqjc7QTKBD9TDFO"
        henry_customer_id = "cus_PZV6GO3wuec92B"

        me = stripe.Customer.retrieve(henry_customer_id)
        randint = random.randint(10, 30)
        print(f"這次付款的比率是: {randint}")

        invoice_item = stripe.InvoiceItem.create(
            customer=me.stripe_id,
            amount=int( randint * 100),  # 轉換為最小貨幣單位
            currency='usd',
            description=f"Subscription for remaining days of month"
        )


        single_day_fee_product = "prod_Paxo32goteCcK3"
        milk_every_month_100usd = "price_1OlShNBFkLqjc7QTcBirlV2I"


        formal_every_month = "price_1OllxWBFkLqjc7QT6cQwKxLo"

        idp_key = f"omg-mooo-{random.randint(1, 10000000)}"
        checkout_session = stripe.checkout.Session.create(
            stripe_account=me.stripe_account,
            customer_email=me.email,
            idempotency_key=f"omg-mooo-{random.randint(1, 10000000)}",
            line_items=[
                {
                    'price': formal_every_month,
                    'quantity': 1,
                },
                {
                    'price_data': { # 一次性費用的定義
                        'currency': 'usd',
                        'product_data': {
                            'name': '當月剩餘天數所需費用',
                            # 'name': 'Charge for the Remaining Days of the Month',
                        },
                        'unit_amount': 15, # 一次性費用的金額，例如 $15.00 USD
                    },
                    'quantity': 10,
                }
            ],
            mode='subscription',
            subscription_data={
                "trial_period_days": 25 - datetime.datetime.now().day,
                # "billing_cycle_anchor": get_next_month_timestamp(25),
                # "billing_cycle_anchor": int(round( (datetime.datetime.now() + datetime.timedelta(days=5)).timestamp() )),
                "description": "YOOOOO - " + idp_key
            },
            billing_address_collection="required",
            phone_number_collection={"enabled": True},
            success_url=f"{DOMAIN}/shop/success" + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url= f"{DOMAIN}/shop/cancel",
        )

        return JsonResponse({
            "redirect": checkout_session.url
        })

@method_decorator(csrf_exempt, name='dispatch')
class AttachPaymentMethod(View):
    def get(self, request, *args, **kwargs):
        return render(request, "attach-payment.html", context={})
    
    def post(self, request, *args, **kwargs): 

        data = json.loads(request.body)

        # print(data["paymentMethodId"])

        
        return JsonResponse({
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

        import json
        with open("events/{event['type']}.json", "w", encoding="utf-8") as f:
            json.dump(event, f)


        if event["type"] in [
            "customer.subscription.updated",
            "customer.subscription.created"
        ]:
            print(event)

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
        if event['type'] == 'invoice.payment_succeeded':
            print("Yoooooooo ---------------- !!!!!!!!!!!!!!!!!!!")
            # print(event)

            subscription_id = event["data"]["object"]["subscription"]
            sub = stripe.Subscription.retrieve(event["data"]["object"]["subscription"])
            # invoices = stripe.Invoice.list(subscription=event["data"]["object"]["subscription"])
            # for x in invoices.auto_paging_iter():
            #     print(x)



            # print("------", len(list(invoices.auto_paging_iter())) )
            # if len(list(invoices.auto_paging_iter())) == 6:
            #     trial_end = datetime.datetime.now() + datetime.timedelta(days=180)  # 例如，180天后
            #     updated_subscription = stripe.Subscription.modify(
            #     subscription_id,
            #     trial_end=int(trial_end.timestamp()),
            #     )


            # print(dir(x)) 
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