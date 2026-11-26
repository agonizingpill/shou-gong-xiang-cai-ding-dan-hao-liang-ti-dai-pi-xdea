from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class EstimateLoss(BaseModel):
    model_config = ConfigDict(extra="forbid")
    order_ref: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    lot: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class FileLoss(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    token: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
