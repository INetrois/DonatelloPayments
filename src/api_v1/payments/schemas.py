from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class PaymentBase(BaseModel):
    amount: float = Field(..., ge=50, le=2000)
    description: str | None = None


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: str
    status: str
    generated_url: str | None
    created_at: datetime
    updated_at: datetime
