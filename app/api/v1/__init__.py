from fastapi import APIRouter
from .endpoints import user, auth, purchase_orders, role, status_order

api_router = APIRouter()

api_router.include_router(role.router, prefix="/role", tags=["role"])
api_router.include_router(status_order.router, prefix="/status_order", tags=["status_order"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(purchase_orders.router, prefix="/purchase_orders", tags=["purchase_orders"])