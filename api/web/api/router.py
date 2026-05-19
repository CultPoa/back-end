from fastapi.routing import APIRouter

from api.web.api import monitoring, users, places, badges

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(places.router)
api_router.include_router(badges.router)
