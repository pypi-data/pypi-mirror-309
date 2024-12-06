# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Subscription", "Result", "ResultCycle", "ResultRetryStrategy"]


class ResultCycle(BaseModel):
    amount: Optional[float] = None
    """Payment amount"""

    payment_id: Optional[str] = FieldInfo(alias="paymentId", default=None)
    """Payment Id"""

    payment_state: Optional[
        Literal["CHECKOUT", "PENDING", "CANCELLED", "DECLINED", "COMPLETED"]
    ] = FieldInfo(alias="paymentState", default=None)
    """Payment State"""

    sequence: Optional[int] = None
    """Sequence number of the cycle"""

    start_time: Optional[str] = FieldInfo(alias="startTime", default=None)
    """
    Date and time when this cycle was supposed to be created according to the
    schedule
    """

    type: Optional[Literal["REGULAR", "RETRY"]] = None
    """Cycle type"""


class ResultRetryStrategy(BaseModel):
    frequency: int
    """
    The number of intervals after which the system will retry the payment after an
    unsuccessful attempt
    """

    number_of_cycles: int = FieldInfo(alias="numberOfCycles")
    """Required number of retries"""

    amount_adjustments: Optional[List[int]] = FieldInfo(
        alias="amountAdjustments", default=None
    )
    """
    If specified, the nth element contains the percentage of the initial amount that
    will be charged for the nth retry
    """

    frequency_unit: Optional[Literal["MINUTE", "DAY", "WEEK", "MONTH"]] = FieldInfo(
        alias="frequencyUnit", default=None
    )
    """The interval at which the subscription is retried.

    Use 'MINUTE' for testing purposes only.
    """


class Result(BaseModel):
    id: Optional[str] = None
    """Subscription Id"""

    amount: Optional[float] = None
    """The amount to be used for subsequent payments"""

    create_time: Optional[str] = FieldInfo(alias="createTime", default=None)
    """Date and time the subscription was created"""

    currency: Optional[str] = None
    """Payment currency"""

    customer_reference_id: Optional[str] = FieldInfo(
        alias="customerReferenceId", default=None
    )
    """Id of the customer from initial payment"""

    cycles: Optional[List[ResultCycle]] = None
    """List of payments automatically generated for this subscription"""

    description: Optional[str] = None
    """Description for subsequent recurring payments"""

    frequency: Optional[int] = None
    """The number of intervals after which a subscriber is billed.

    For example, if the frequencyUnit is DAY with an frequency of 2, the
    subscription is billed once every two days.
    """

    frequency_unit: Optional[Literal["MINUTE", "DAY", "WEEK", "MONTH"]] = FieldInfo(
        alias="frequencyUnit", default=None
    )
    """The interval at which the subscription is billed.

    Use 'MINUTE' for testing purposes only.
    """

    recurring_token: Optional[str] = FieldInfo(alias="recurringToken", default=None)
    """Token that is used to continue the recurring chain"""

    requested_number_of_cycles: Optional[int] = FieldInfo(
        alias="requestedNumberOfCycles", default=None
    )
    """Required number of subsequent recurring payments.

    Unlimited if value is not specified.
    """

    retry_strategy: Optional[ResultRetryStrategy] = FieldInfo(
        alias="retryStrategy", default=None
    )
    """Retry strategy for subscription.

    If not specified, the subscription is canceled after the first failed payment
    attempt.
    """

    start_time: Optional[str] = FieldInfo(alias="startTime", default=None)
    """Date and time of the 1st cycle"""

    state: Optional[Literal["ACTIVE", "CANCELLED", "COMPLETED"]] = None
    """Subscription state"""


class Subscription(BaseModel):
    result: Optional[Result] = None

    status: Optional[int] = None
    """HTTP status code"""

    timestamp: Optional[str] = None
