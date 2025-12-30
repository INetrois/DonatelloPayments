from fastapi import APIRouter

from .payments.views import router as payments_router
from .donatello.views import router as donatello_router

router = APIRouter()
router.include_router(payments_router, prefix="/payments")
router.include_router(donatello_router, prefix="/donatello")
