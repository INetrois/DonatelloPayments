from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from . import crud
from .schemas import Payment, PaymentCreate

router = APIRouter(tags=["Payments"])


@router.get("/", response_model=list[Payment])
async def get_payments(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[Payment]:
    return await crud.get_payments(session=session)


@router.post("/", response_model=Payment)
async def create_payment(
    amount: float,
    description: str | None = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Payment:
    if amount < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be at least 50!",
        )

    payment_in = PaymentCreate(amount=amount, description=description)
    return await crud.create_payment(session=session, payment_in=payment_in)
