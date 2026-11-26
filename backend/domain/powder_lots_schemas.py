from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class ReceiveLot(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    material: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    scent: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    declaration: list | dict
    moisture: FiniteFloat
    batch_grams: int
