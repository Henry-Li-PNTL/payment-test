
import stripe
stripe.api_key = "sk_test_51OZTUEBFkLqjc7QTFXwxu3Me4oCgklY5DLs5jqAUEkYky5e4VBfyAE5FHpp99Kc8RUqOlxvoHGDRtDHOJAnhFvGJ00YkqrxM0U"

# 创建客户（如果已存在，则跳过）
# me = stripe.Customer.create(
#     email="henryliking@gmail.com",
# )


me = stripe.Customer.retrieve("cus_PZV6GO3wuec92B")
print(me)

xxxx = stripe.InvoiceItem.create(
    customer=me.stripe_id,
    amount=int(14.2 * 100),  # 轉換為最小貨幣單位
    currency='usd',
    description=f"Subscription for remaining days of month"
)

subscription = stripe.Subscription.create(
    customer=me.stripe_id,
    items=[{
        'price': 'price_1OetlBBFkLqjc7QTKBD9TDFO',  # 每月300元的定价ID
    }],
    add_invoice_items=[xxxx.stripe_id],
    # 可以设置其他订阅参数，如试用期等
)


subscription

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
plan = stripe.Plan.create(
  amount=1200,
  currency="usd",
  interval="day",
  interval_count=3,
  product="prod_PTrUBPTEJuplWc",
)

print(plan)
