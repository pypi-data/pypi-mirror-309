# Payments

Types:

```python
from mtn_payments_v1.types import (
    InboundResponse,
    OrderResponse,
    PaymentResponse,
    PaymentTransactionStatusResponse,
)
```

Methods:

- <code title="post /payments">client.payments.<a href="./src/mtn_payments_v1/resources/payments/payments.py">create</a>(\*\*<a href="src/mtn_payments_v1/types/payment_create_params.py">params</a>) -> <a href="./src/mtn_payments_v1/types/payment_response.py">PaymentResponse</a></code>
- <code title="post /payments/fee">client.payments.<a href="./src/mtn_payments_v1/resources/payments/payments.py">fee</a>(\*\*<a href="src/mtn_payments_v1/types/payment_fee_params.py">params</a>) -> <a href="./src/mtn_payments_v1/types/inbound_response.py">InboundResponse</a></code>
- <code title="post /payments/payment-link">client.payments.<a href="./src/mtn_payments_v1/resources/payments/payments.py">payment_link</a>(\*\*<a href="src/mtn_payments_v1/types/payment_payment_link_params.py">params</a>) -> <a href="./src/mtn_payments_v1/types/order_response.py">OrderResponse</a></code>
- <code title="get /payments/{correlatorId}/transactionStatus">client.payments.<a href="./src/mtn_payments_v1/resources/payments/payments.py">transaction_status</a>(correlator_id, \*\*<a href="src/mtn_payments_v1/types/payment_transaction_status_params.py">params</a>) -> <a href="./src/mtn_payments_v1/types/payment_transaction_status_response.py">PaymentTransactionStatusResponse</a></code>

## History

Types:

```python
from mtn_payments_v1.types.payments import PaymentHistoryResponse
```

Methods:

- <code title="get /payments/{id}/history">client.payments.history.<a href="./src/mtn_payments_v1/resources/payments/history.py">list</a>(id, \*\*<a href="src/mtn_payments_v1/types/payments/history_list_params.py">params</a>) -> <a href="./src/mtn_payments_v1/types/payments/payment_history_response.py">PaymentHistoryResponse</a></code>

## PaymentAgreement

Types:

```python
from mtn_payments_v1.types.payments import PromiseToPayEligibilityResponse, PromiseToPayResponse
```

Methods:

- <code title="post /payments/payment-agreement">client.payments.payment_agreement.<a href="./src/mtn_payments_v1/resources/payments/payment_agreement.py">create</a>(\*\*<a href="src/mtn_payments_v1/types/payments/payment_agreement_create_params.py">params</a>) -> <a href="./src/mtn_payments_v1/types/payments/promise_to_pay_response.py">PromiseToPayResponse</a></code>
- <code title="get /payments/payment-agreement/eligibility">client.payments.payment_agreement.<a href="./src/mtn_payments_v1/resources/payments/payment_agreement.py">eligibility</a>(\*\*<a href="src/mtn_payments_v1/types/payments/payment_agreement_eligibility_params.py">params</a>) -> <a href="./src/mtn_payments_v1/types/payments/promise_to_pay_eligibility_response.py">PromiseToPayEligibilityResponse</a></code>

# ReversePayments

Types:

```python
from mtn_payments_v1.types import ReverseTransactionHistory
```

Methods:

- <code title="get /reverse-payment/history">client.reverse_payments.<a href="./src/mtn_payments_v1/resources/reverse_payments.py">history</a>(\*\*<a href="src/mtn_payments_v1/types/reverse_payment_history_params.py">params</a>) -> <a href="./src/mtn_payments_v1/types/reverse_transaction_history.py">ReverseTransactionHistory</a></code>
