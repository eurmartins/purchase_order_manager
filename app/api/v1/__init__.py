from fastapi import APIRouter
from .endpoints import user, auth, purchase_orders

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(purchase_orders.router,  prefix="/purchase_orders", tags=["purchase_orders"])