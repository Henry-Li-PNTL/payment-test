import stripe

secret_key = "sk_test_51OZTUEBFkLqjc7QTFXwxu3Me4oCgklY5DLs5jqAUEkYky5e4VBfyAE5FHpp99Kc8RUqOlxvoHGDRtDHOJAnhFvGJ00YkqrxM0U"
stripe.api_key = secret_key

# 假设你已经有了一个订阅ID
subscription_id = "sub_1OgJ0TBFkLqjc7QTD9AcxAoG"

# 获取订阅对象
subscription = stripe.Subscription.retrieve(subscription_id)
# print(dir(subscription))

# 使用订阅对象中的客户ID获取客户对象
customer_id = subscription.customer
customer = stripe.Customer.retrieve(customer_id)

# 获取默认支付方式
default_payment_method = customer.invoice_settings.default_payment_method
payment_method = stripe.PaymentMethod.retrieve(default_payment_method)

# 打印支付方式的详细信息
print("Card Brand:", payment_method.card.brand)
print("Last 4:", payment_method.card.last4)
print("Exp Month:", payment_method.card.exp_month)
print("Exp Year:", payment_method.card.exp_year)




payment_method = stripe.PaymentMethod.retrieve(subscription.to_dict()["default_payment_method"])

# 打印支付方式的详细信息
print("Card Brand:", payment_method.card.brand)
print("Last 4:", payment_method.card.last4)
print("Exp Month:", payment_method.card.exp_month)
print("Exp Year:", payment_method.card.exp_year)



invoices = stripe.Invoice.list(customer='cus_xxx')
for invoice in invoices.auto_paging_iter():
    print(invoice)