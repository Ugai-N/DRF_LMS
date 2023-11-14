import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from lms.models import Payment

stripe.api_key = settings.STRIPE_API_KEY
endpoint_secret = settings.STRIPE_ENDPOINT


def create_checkout_session(request):
    checkout_session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    # вместо product_data можно просто указать product -> product_ID если его создавать при
                    # создании уроков и курсов + сохранять в модели продукта)
                    "product_data": {
                        "name": "lesson 3",
                        "description": "lesson 3 description"
                    },
                    "unit_amount": request.data['amount_paid']  # можно делать ретрив из ID продукта
                    # с дефолтной ценой
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        # ui_mode='hosted'
    )
    request.data['payment_link'] = checkout_session.url
    request.data['payment_session_stripe_id'] = checkout_session.id
    return request


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        if session.payment_status == "paid":
            # Fulfill the purchase
            fulfill_order(session)

        elif event['type'] == 'checkout.session.async_payment_succeeded':
            session = event['data']['object']

            # Fulfill the purchase
            fulfill_order(session)

        elif event['type'] == 'checkout.session.async_payment_failed':
            session = event['data']['object']

            # smth else, e.g. Send an email to the customer asking them to retry their order

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    payment_obj = Payment.objects.get(payment_session_stripe_id=session.id)
    payment_obj.payment_status = 'succeed'
    payment_obj.save()

    # retrieve_report = stripe.checkout.Session.retrieve(session.id)
    # print(f'checkout_session.id при оплате: {session.id}')
    # print(f'retrieve_report сессии при оплате: {retrieve_report}')
    # print(f'ссылка на сессию после оплаты {retrieve_report.url}') #NONE

