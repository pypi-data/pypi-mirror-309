from typing import Optional
from pydantic import BaseModel


class CreatePayment(BaseModel):
    currency: str = "rub"
    amount: str
    uuid: str
    shopId: int
    description: str
    subscribe: Optional[str] = None
    holdTime: Optional[str] = None

