"""Application middleware for request tracking and error handling."""
import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import bind_request_context, get_logger

logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add request ID to each request."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        # Bind request context for structured logging
        bind_request_context(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests with timing."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()
        
        response = await call_next(request)
        
        process_time = (time.perf_counter() - start_time) * 1000
        
        # Log request completion
        logger.info(
            "request_completed",
            status_code=response.status_code,
            duration_ms=round(process_time, 2),
            client_ip=request.client.host if request.client else None,
        )
        
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled errors."""
    request_id = getattr(request.state, "request_id", None)
    
    logger.exception(
        "unhandled_exception",
        error=str(exc),
        error_type=type(exc).__name__,
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred",
            "request_id": request_id,
        },
    )


def setup_middleware(app: FastAPI) -> None:
    """Configure all middleware for the application."""
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)
    
    # Add global exception handler
    app.add_exception_handler(Exception, global_exception_handler)
