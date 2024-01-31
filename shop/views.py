import stripe

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

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
          payment_intent = event['data']['object']
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event['type']))

        return JsonResponse({
            "success": True
        })
