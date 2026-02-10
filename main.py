# import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.base_exception import AppException

from app.api.routes import router as test_router
from app.api.v1 import auth_router, user_router, parlon_router


app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE","PATCH"],
    allow_headers=["Content-Type","X-CSRF-Token","X-Client-Type"],
)


@app.get("/api")
def root():
    return settings.dict()

app.include_router(test_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(parlon_router)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message
        }
    )

@app.middleware("http")
async def check_client_type(request: Request, call_next):
    auth_header = request.headers.get("Authorization", "").lower()

    if auth_header.startswith("bearer "):
        client_type = "app"
    else:
        client_type = "browser"

    request.state.client_type = client_type
    # breakpoint()
    return await call_next(request)