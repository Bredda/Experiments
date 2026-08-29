"""API v1 router aggregation."""
# ruff: noqa: I001 - Imports structured for Jinja2 template conditionals

from fastapi import APIRouter

from .health import router as health_router
from .runs import router as runs_router

api_router = APIRouter(prefix="/api")

# Health check routes
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(runs_router, tags=["Runs"])