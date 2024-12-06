# Payments

Types:

```python
from paymaxis.types import Payment, PaymentListResponse
```

Methods:

- <code title="post /api/v1/payments">client.payments.<a href="./src/paymaxis/resources/payments/payments.py">create</a>(\*\*<a href="src/paymaxis/types/payment_create_params.py">params</a>) -> <a href="./src/paymaxis/types/payment.py">Payment</a></code>
- <code title="get /api/v1/payments/{id}">client.payments.<a href="./src/paymaxis/resources/payments/payments.py">retrieve</a>(id) -> <a href="./src/paymaxis/types/payment.py">Payment</a></code>
- <code title="get /api/v1/payments">client.payments.<a href="./src/paymaxis/resources/payments/payments.py">list</a>(\*\*<a href="src/paymaxis/types/payment_list_params.py">params</a>) -> <a href="./src/paymaxis/types/payment_list_response.py">PaymentListResponse</a></code>

## Operations

Types:

```python
from paymaxis.types.payments import Operation
```

Methods:

- <code title="get /api/v1/payments/{id}/operations">client.payments.operations.<a href="./src/paymaxis/resources/payments/operations.py">list</a>(id) -> <a href="./src/paymaxis/types/payments/operation.py">Operation</a></code>

# Subscriptions

Types:

```python
from paymaxis.types import Subscription
```

Methods:

- <code title="get /api/v1/subscriptions/{id}">client.subscriptions.<a href="./src/paymaxis/resources/subscriptions.py">retrieve</a>(id) -> <a href="./src/paymaxis/types/subscription.py">Subscription</a></code>
- <code title="patch /api/v1/subscriptions/{id}">client.subscriptions.<a href="./src/paymaxis/resources/subscriptions.py">update</a>(id, \*\*<a href="src/paymaxis/types/subscription_update_params.py">params</a>) -> <a href="./src/paymaxis/types/subscription.py">Subscription</a></code>
