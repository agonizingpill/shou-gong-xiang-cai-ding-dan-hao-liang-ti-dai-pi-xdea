from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class ReceiveOrder(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    grams: int
    scent: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    declaration: list | dict
    dryer: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class ClearHold(BaseModel):
    model_config = ConfigDict(extra="forbid")
    order_ref: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    reason: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
