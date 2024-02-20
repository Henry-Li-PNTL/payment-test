import random
import stripe
import datetime


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

stripe.api_key = "sk_test_51OZTUEBFkLqjc7QTFXwxu3Me4oCgklY5DLs5jqAUEkYky5e4VBfyAE5FHpp99Kc8RUqOlxvoHGDRtDHOJAnhFvGJ00YkqrxM0U"

secret_key = "sk_test_51OZTUEBFkLqjc7QTFXwxu3Me4oCgklY5DLs5jqAUEkYky5e4VBfyAE5FHpp99Kc8RUqOlxvoHGDRtDHOJAnhFvGJ00YkqrxM0U"
stripe.api_key = secret_key



# 创建客户（如果已存在，则跳过）
# me = stripe.Customer.create(
#     email="henryliking@gmail.com",
# )

formal_every_month_100usd = "price_1OllxWBFkLqjc7QT6cQwKxLo"

milk_every_day_10usd = "price_1OetlBBFkLqjc7QTKBD9TDFO"
milk_every_day_20usd = "plan_PacHbLUFAr6vX7"
milk_every_4day_10usd = "plan_PacNQZGwSprCnS"
milk_every_month_100usd = "price_1OlShNBFkLqjc7QTcBirlV2I"
using_price = formal_every_month_100usd
henry_customer_id = "cus_PZV6GO3wuec92B"

single_day_fee_product = "prod_Paxo32goteCcK3"

me = stripe.Customer.retrieve(henry_customer_id)
print(me)

# 添加支付方式
# 不能直接這樣使用，不安全 所以會被擋下來，要額外開通
# stripe.error.CardError: Request req_Om49RImIKH4R1h: 
# Sending credit card numbers directly to the Stripe API is generally unsafe. 
# We suggest you use test tokens that map to the test card you are using, 
# see https://stripe.com/docs/testing. To enable raw card data APIs in test mode, see https://support.stripe.com/questions/enabling-access-to-raw-card-data-apis.
# payment_method = stripe.PaymentMethod.create(
#     type="card",
#     card={
#         "number": "4242424242424242",
#         "exp_month": 12,
#         "exp_year": 2025,
#         "cvc": "123",
#     },
# )

# stripe.PaymentMethod.attach(
#     payment_method.id,
#     customer=me.stripe_id,
# )


randint = random.randint(10, 30)
print(f"這次付款的比率是: {randint}")
invoice_item = stripe.InvoiceItem.create(
    customer=me.stripe_id,
    amount=int( randint * 100),  # 轉換為最小貨幣單位
    currency='usd',
    description=f"額外買牛奶 - {datetime.datetime.now().strftime('%m%d-%H%M')}"
)

# subscription = stripe.Subscription.create(
#     customer=me.stripe_id,
#     items=[{
#         'price': using_price,  # 每月10元的定价ID
#     }],
#     # add_invoice_items=[xxxx.stripe_id],
#     # 可以设置其他订阅参数，如试用期等
# )
# subscription


me.stripe_account


idp_key = f"omg-mooo-{random.randint(1, 10000000)}"
DOMAIN = "http://127.0.0.1:8000"
checkout_session = stripe.checkout.Session.create(
            stripe_account=me.stripe_account,
            customer_email=me.email,
            idempotency_key=idp_key,
            line_items=[
                {
                    'price': using_price,
                    'quantity': 1,
                },
                # {
                #     'price_data': {
                #         "currency": "USD",
                #         "product": single_day_fee_product,
                #         "unit_amount": 1100,
                #     },
                #     'quantity': 5,
                # },
            ],
            mode='subscription',
            subscription_data={
                # "trial_period_days": 2,
                "billing_cycle_anchor": get_next_month_timestamp(25),
                # "billing_cycle_anchor": int(round( (datetime.datetime.now() + datetime.timedelta(days=5)).timestamp() )),
                "description": "YOOOOO - " + idp_key
            },
            billing_address_collection="required",
            phone_number_collection={"enabled": True},
            success_url=f"{DOMAIN}/shop/success" + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url= f"{DOMAIN}/shop/cancel",
        )


print(checkout_session.url)

# # 创建订阅时添加一次性费用
# subscription = stripe.Subscription.create(
#     customer=me.stripe_id,
#     items=[{
#         'price': 'price_XXXX',  # 每月300元的定价ID
#     }],
#     # add_invoice_items=[{
#     #     'price_data': {
#     #         'currency': 'usd',
#     #         'product': 'prod_XXXX',  # 产品ID
#     #         'unit_amount': 300,  # 额外的一次性费用
#     #         'recurring': {'interval': 'month'},
#     #     },
#     # }],
#     # 可以设置其他订阅参数，如试用期等
# )

# print(subscription)




# Create a Plan
# plan = stripe.Plan.create(
#   amount=1000,
#   currency="usd",
#   interval="day",
#   interval_count=4,
#   product="prod_PTrUBPTEJuplWc",
# )

# print(plan)






# WEBHOOK LOCAL
# stripe listen --forward-to localhost:8000/shop/webhook






