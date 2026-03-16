from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .parlon_routes import router as parlon_router
from .main_category_routes import router as main_category_router

__all__ = ["auth_router", "user_router", "parlon_router","main_category_router"]
