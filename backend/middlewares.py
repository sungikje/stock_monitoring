# middlewares.py

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from backend.utils.jwt import decode_token

EXCLUDE_PREFIXES = ["/api/login", "/api/signup", "/static", "/docs", "/openapi.json"]


class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("🚀 middleware triggered:", request.url.path)

        if request.method == "OPTIONS":
            return await call_next(request)

        for path in EXCLUDE_PREFIXES:
            if request.url.path.startswith(path):
                return await call_next(request)

        token = request.headers.get("Authorization")
        if token:
            token = token.replace("Bearer ", "")
            payload = decode_token(token)
            if payload:
                request.state.user = payload
                return await call_next(request)

        return JSONResponse({"detail": "Unauthorized"}, status_code=401)
