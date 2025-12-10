from fastapi import APIRouter

from app.api.routes import (
    auth,
    categories,
    customers,
    parts,
    purchase_invoices,
    reports,
    sales_invoices,
    stock_adjustments,
    suppliers,
    tractor_models,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(categories.router, prefix='/categories', tags=['categories'])
api_router.include_router(tractor_models.router, prefix='/tractor-models', tags=['tractor-models'])
api_router.include_router(suppliers.router, prefix='/suppliers', tags=['suppliers'])
api_router.include_router(customers.router, prefix='/customers', tags=['customers'])
api_router.include_router(parts.router, prefix='/parts', tags=['parts'])
api_router.include_router(purchase_invoices.router, prefix='/purchase-invoices', tags=['purchase-invoices'])
api_router.include_router(sales_invoices.router, prefix='/sales-invoices', tags=['sales-invoices'])
api_router.include_router(stock_adjustments.router, prefix='/stock-adjustments', tags=['stock-adjustments'])
api_router.include_router(reports.router, prefix='/reports', tags=['reports'])
