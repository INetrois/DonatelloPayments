"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Payment

from .schemas import PaymentCreate


# -------------------
#        Read
# -------------------
async def get_payments(session: AsyncSession) -> list[Payment]:
    stmt = select(Payment).order_by(Payment.created_at.desc())
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_payment(session: AsyncSession, payment_id: int) -> Payment | None:
    return await session.get(Payment, payment_id)


# -------------------
#        Create
# -------------------
async def create_payment(session: AsyncSession, payment_in: PaymentCreate) -> Payment:
    payment = Payment(**payment_in.model_dump())
    session.add(payment)
    await session.commit()
    await session.refresh(payment)
    return payment


# -------------------
#        Update
# -------------------
async def update_payment(
    session: AsyncSession, payment: Payment, fields_to_update: dict
) -> Payment:
    for field, value in fields_to_update.items():
        setattr(payment, field, value)

    session.add(payment)
    await session.commit()
    await session.refresh(payment)
    return payment
