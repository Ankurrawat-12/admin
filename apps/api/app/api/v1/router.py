"""API v1 router that combines all endpoint modules."""
from fastapi import APIRouter

from app.api.v1.endpoints import audit, auth, dashboard, projects, users

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(projects.router)
api_router.include_router(audit.router)
api_router.include_router(dashboard.router)
