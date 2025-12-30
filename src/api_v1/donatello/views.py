from pprint import pprint
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
from urllib.parse import parse_qs

from core.config import settings
from core.models import Payment, db_helper

from .services import generate_url

router = APIRouter(tags=["Donatello"])


@router.post("/")
async def generate_donatello_link(
    payment_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    payment: Payment | None = await session.get(Payment, payment_id)

    if payment.generated_url is not None:
        return {"url4payment": payment.generated_url}

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with id {payment_id} not found!",
        )

    url = await generate_url(
        donatello_user=settings.donatello_user,
        uuid=payment.uuid,
        amount=payment.amount,
    )

    payment.generated_url = url
    payment.status = "processing"
    
    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    return {"url4payment": url}


@router.post("/callback/")
async def handle_donatello_callback(
    request: Request, session: AsyncSession = Depends(db_helper.session_dependency)
):
    try:
        body_bytes = await request.body()

        try:
            payload = await request.json()
        except Exception:
            payload = body_bytes.decode(errors="replace")
    except Exception as exc:
        print("Error reading callback body:", exc)
        payload = None

    payload_dict = {}
    if isinstance(payload, dict):
        payload_dict = payload
    elif isinstance(payload, str):
        try:
            payload_dict = json.loads(payload)
        except Exception:
            parsed = parse_qs(payload)
            payload_dict = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

    if getattr(settings, "debug", False):
        pprint(payload_dict)
    
    payment_sender = payload_dict.get("clientName")
    payment_uuid = payload_dict.get("message")
    payment_amount = payload_dict.get("amount")

    if not payment_uuid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing payment uuid in callback payload",
        )

    result = await session.execute(
        select(Payment).where(Payment.uuid == payment_uuid)
    )
    payment: Payment | None = result.scalar_one_or_none()

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not DonatelloPayments callback!",
        )
    
    if payment_sender != settings.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sender mismatch! (Please report)",
        )

    try:
        if payment_amount is None or float(payment_amount) != float(payment.amount):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount mismatch! (Please report)",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid amount format in callback payload",
        )

    payment.status = "success"
    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    return {"status": "success"}
