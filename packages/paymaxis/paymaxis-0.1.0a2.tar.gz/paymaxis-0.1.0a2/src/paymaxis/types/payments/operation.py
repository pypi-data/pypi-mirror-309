# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["Operation", "Result"]


class Result(BaseModel):
    id: Optional[int] = None
    """Operation Id"""

    completed: Optional[str] = None
    """Operation end time"""

    incoming_messages: Optional[str] = FieldInfo(alias="incomingMessages", default=None)
    """List of messages received from external APIs during operation processing"""

    operation: Optional[
        Literal[
            "CREATE_PAYMENT",
            "CHECKOUT",
            "CANCEL",
            "CONFIRMATION",
            "CASCADING",
            "REDIRECT",
            "CONTINUE",
            "CONTINUE_ANTI_FRAUD",
            "DETECT_FRAUD",
            "DEPOSIT",
            "WITHDRAWAL",
            "REFUND",
            "CHARGEBACK",
            "CHECK_STATE",
            "HANDLE_WEBHOOK",
            "MANUAL_UPDATE",
        ]
    ] = None
    """Operation performed during payment processing"""

    outgoing_messages: Optional[str] = FieldInfo(alias="outgoingMessages", default=None)
    """List of messages sent to external APIs during operation processing"""

    payment_state: Optional[
        Literal["CHECKOUT", "PENDING", "CANCELLED", "DECLINED", "COMPLETED"]
    ] = FieldInfo(alias="paymentState", default=None)
    """Payment State"""

    started: Optional[str] = None
    """Operation start time"""


class Operation(BaseModel):
    result: Optional[List[Result]] = None

    status: Optional[int] = None
    """HTTP status code"""

    timestamp: Optional[str] = None
