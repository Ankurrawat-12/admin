# Admin Panel - Complete Technical Reference

> **This document explains EVERYTHING about this project - every file, every function, every configuration, every line of code.**

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Complete Technology Stack](#2-complete-technology-stack)
3. [Project Structure](#3-project-structure)
4. [Docker Configuration](#4-docker-configuration)
5. [Backend - Complete Reference](#5-backend---complete-reference)
6. [Frontend - Complete Reference](#6-frontend---complete-reference)
7. [Database - Complete Reference](#7-database---complete-reference)
8. [Authentication System](#8-authentication-system)
9. [Authorization (RBAC) System](#9-authorization-rbac-system)
10. [API Reference](#10-api-reference)
11. [Error Handling](#11-error-handling)
12. [Logging & Observability](#12-logging--observability)
13. [Security Considerations](#13-security-considerations)
14. [Performance Optimizations](#14-performance-optimizations)
15. [Testing Guide](#15-testing-guide)
16. [Deployment - Complete Guide](#16-deployment---complete-guide)
17. [Maintenance & Operations](#17-maintenance--operations)
18. [Extending the Project](#18-extending-the-project)
19. [Troubleshooting Encyclopedia](#19-troubleshooting-encyclopedia)
20. [Glossary](#20-glossary)

---

# 1. Project Overview

## What is this project?

This is a **production-ready admin panel** - a web application that allows administrators to manage users, projects, and view audit logs. It's the type of internal tool that companies use to manage their business operations.

## Key Features

| Feature | Description |
|---------|-------------|
| **User Management** | Create, read, update, delete users with different roles |
| **Project Management** | Full CRUD for projects with status and priority tracking |
| **Role-Based Access Control** | Three roles (Admin, Manager, Viewer) with different permissions |
| **Audit Logging** | Every sensitive action is logged for compliance |
| **JWT Authentication** | Secure token-based authentication with refresh tokens |
| **Dark Mode** | User-selectable light/dark theme |
| **Responsive Design** | Works on desktop, tablet, and mobile |
| **Real-time Validation** | Forms validate as you type |
| **Optimistic Updates** | UI updates immediately, syncs with server in background |

## Demo Credentials

| Role | Email | Password | What they can do |
|------|-------|----------|------------------|
| **Admin** | admin@example.com | admin123 | Everything - full system access |
| **Manager** | manager@example.com | manager123 | Create/edit own projects, view users |
| **Viewer** | viewer@example.com | viewer123 | View only - cannot modify anything |

---

# 2. Complete Technology Stack

## Backend Technologies

| Technology | Version | Purpose | Why we chose it |
|------------|---------|---------|-----------------|
| **Python** | 3.12 | Programming language | Modern, async support, great ecosystem |
| **FastAPI** | 0.109.0 | Web framework | Fastest Python framework, auto-docs, type hints |
| **SQLAlchemy** | 2.0 | ORM (Object-Relational Mapping) | Industry standard, async support |
| **Pydantic** | 2.5 | Data validation | Automatic validation, serialization |
| **Alembic** | 1.13 | Database migrations | SQLAlchemy's official migration tool |
| **asyncpg** | 0.29 | PostgreSQL driver | Fastest async PostgreSQL driver |
| **python-jose** | 3.3 | JWT handling | Standard JWT library |
| **passlib** | 1.7 | Password hashing | Secure bcrypt implementation |
| **structlog** | 24.1 | Structured logging | JSON logs, context binding |
| **uvicorn** | 0.27 | ASGI server | High-performance async server |

## Frontend Technologies

| Technology | Version | Purpose | Why we chose it |
|------------|---------|---------|-----------------|
| **React** | 18.2 | UI library | Industry standard, huge ecosystem |
| **TypeScript** | 5.3 | Type-safe JavaScript | Catches errors at compile time |
| **Vite** | 5.0 | Build tool | Fastest dev server, optimized builds |
| **TailwindCSS** | 3.4 | CSS framework | Utility-first, highly customizable |
| **shadcn/ui** | Latest | Component library | Beautiful, accessible, customizable |
| **React Query** | 5.17 | Server state management | Caching, background refetch, optimistic updates |
| **React Router** | 6.21 | Client-side routing | Standard React routing solution |
| **React Hook Form** | 7.49 | Form handling | Performance-focused, minimal re-renders |
| **Zod** | 3.22 | Schema validation | TypeScript-first validation |
| **Lucide React** | 0.303 | Icons | Beautiful, consistent icon set |

## Infrastructure Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Docker** | 24+ | Containerization |
| **Docker Compose** | 2.23+ | Multi-container orchestration |
| **PostgreSQL** | 16 | Primary database |
| **Redis** | 7 | Caching, session storage |
| **Nginx** | Alpine | Reverse proxy, static file serving |

---

# 3. Project Structure

## Complete Directory Tree

```
admin_panel/
│
├── 📄 docker-compose.yml          # Docker services configuration
├── 📄 README.md                   # Quick start guide
├── 📄 DOCUMENTATION.md            # Detailed documentation
├── 📄 TECHNICAL_REFERENCE.md      # This file - complete reference
│
├── 📁 apps/
│   │
│   ├── 📁 api/                    # ═══ BACKEND ═══
│   │   │
│   │   ├── 📄 Dockerfile          # Container build instructions
│   │   ├── 📄 requirements.txt    # Python dependencies
│   │   ├── 📄 alembic.ini         # Alembic configuration
│   │   ├── 📄 seed_db.py          # Database seeding script
│   │   ├── 📄 env.example         # Example environment variables
│   │   │
│   │   ├── 📁 alembic/            # Database migrations
│   │   │   ├── 📄 env.py          # Migration environment setup
│   │   │   ├── 📄 script.py.mako  # Migration template
│   │   │   └── 📁 versions/       # Migration files
│   │   │       └── 📄 001_initial.py
│   │   │
│   │   └── 📁 app/                # Application code
│   │       │
│   │       ├── 📄 __init__.py     # Package marker
│   │       ├── 📄 main.py         # Application entry point
│   │       │
│   │       ├── 📁 core/           # Core functionality
│   │       │   ├── 📄 __init__.py
│   │       │   ├── 📄 config.py   # Settings management
│   │       │   ├── 📄 database.py # Database connection
│   │       │   ├── 📄 security.py # Auth utilities
│   │       │   ├── 📄 logging.py  # Logging setup
│   │       │   └── 📄 middleware.py # Request middleware
│   │       │
│   │       ├── 📁 models/         # Database models
│   │       │   ├── 📄 __init__.py
│   │       │   ├── 📄 user.py     # User model
│   │       │   ├── 📄 project.py  # Project model
│   │       │   └── 📄 audit_log.py # Audit log model
│   │       │
│   │       ├── 📁 schemas/        # Request/Response schemas
│   │       │   ├── 📄 __init__.py
│   │       │   ├── 📄 auth.py     # Auth schemas
│   │       │   ├── 📄 user.py     # User schemas
│   │       │   ├── 📄 project.py  # Project schemas
│   │       │   ├── 📄 audit.py    # Audit schemas
│   │       │   └── 📄 common.py   # Shared schemas
│   │       │
│   │       ├── 📁 services/       # Business logic
│   │       │   ├── 📄 __init__.py
│   │       │   ├── 📄 user_service.py
│   │       │   ├── 📄 project_service.py
│   │       │   └── 📄 audit_service.py
│   │       │
│   │       └── 📁 api/            # API layer
│   │           ├── 📄 __init__.py
│   │           ├── 📄 deps.py     # Dependencies
│   │           └── 📁 v1/
│   │               ├── 📄 __init__.py
│   │               ├── 📄 router.py # Route aggregator
│   │               └── 📁 endpoints/
│   │                   ├── 📄 __init__.py
│   │                   ├── 📄 auth.py
│   │                   ├── 📄 users.py
│   │                   ├── 📄 projects.py
│   │                   ├── 📄 audit.py
│   │                   └── 📄 dashboard.py
│   │
│   └── 📁 web/                    # ═══ FRONTEND ═══
│       │
│       ├── 📄 Dockerfile          # Container build instructions
│       ├── 📄 nginx.conf          # Nginx configuration
│       ├── 📄 package.json        # Node.js dependencies
│       ├── 📄 package-lock.json   # Locked dependency versions
│       ├── 📄 tsconfig.json       # TypeScript config
│       ├── 📄 tsconfig.node.json  # Node TypeScript config
│       ├── 📄 vite.config.ts      # Vite build config
│       ├── 📄 tailwind.config.js  # Tailwind CSS config
│       ├── 📄 postcss.config.js   # PostCSS config
│       ├── 📄 components.json     # shadcn/ui config
│       ├── 📄 index.html          # HTML entry point
│       │
│       ├── 📁 public/             # Static assets
│       │   └── 📄 vite.svg        # Favicon
│       │
│       └── 📁 src/                # Source code
│           │
│           ├── 📄 main.tsx        # React entry point
│           ├── 📄 index.css       # Global styles
│           ├── 📄 vite-env.d.ts   # Vite type definitions
│           │
│           ├── 📁 components/     # React components
│           │   │
│           │   ├── 📁 layout/     # Layout components
│           │   │   ├── 📄 app-layout.tsx
│           │   │   ├── 📄 sidebar.tsx
│           │   │   ├── 📄 header.tsx
│           │   │   ├── 📄 mobile-sidebar.tsx
│           │   │   └── 📄 toaster.tsx
│           │   │
│           │   ├── 📁 ui/         # UI primitives (shadcn)
│           │   │   ├── 📄 badge.tsx
│           │   │   ├── 📄 button.tsx
│           │   │   ├── 📄 card.tsx
│           │   │   ├── 📄 dialog.tsx
│           │   │   ├── 📄 dropdown-menu.tsx
│           │   │   ├── 📄 input.tsx
│           │   │   ├── 📄 label.tsx
│           │   │   ├── 📄 select.tsx
│           │   │   ├── 📄 separator.tsx
│           │   │   ├── 📄 skeleton.tsx
│           │   │   ├── 📄 switch.tsx
│           │   │   ├── 📄 table.tsx
│           │   │   └── 📄 toast.tsx
│           │   │
│           │   ├── 📁 projects/   # Project-specific
│           │   │   └── 📄 project-modal.tsx
│           │   │
│           │   └── 📁 users/      # User-specific
│           │       └── 📄 user-modal.tsx
│           │
│           ├── 📁 contexts/       # React contexts
│           │   ├── 📄 auth-context.tsx
│           │   └── 📄 theme-context.tsx
│           │
│           ├── 📁 hooks/          # Custom hooks
│           │   └── 📄 use-toast.ts
│           │
│           ├── 📁 lib/            # Utilities
│           │   ├── 📄 api.ts      # API client
│           │   ├── 📄 types.ts    # Type definitions
│           │   └── 📄 utils.ts    # Helper functions
│           │
│           └── 📁 pages/          # Page components
│               ├── 📄 login.tsx
│               ├── 📄 dashboard.tsx
│               ├── 📄 projects.tsx
│               ├── 📄 users.tsx
│               ├── 📄 audit-logs.tsx
│               └── 📄 settings.tsx
```

---

# 4. Docker Configuration

## docker-compose.yml - Complete Breakdown

```yaml
# No version specified - uses latest Compose spec

services:
  # ═══════════════════════════════════════════════════════════════
  # DATABASE SERVICE
  # ═══════════════════════════════════════════════════════════════
  db:
    image: postgres:16-alpine          # Official PostgreSQL image (Alpine = smaller)
    container_name: admin_panel_db     # Fixed container name for easy reference
    restart: unless-stopped            # Auto-restart unless manually stopped
    environment:
      POSTGRES_USER: postgres          # Database superuser username
      POSTGRES_PASSWORD: postgres      # Database superuser password
      POSTGRES_DB: admin_panel         # Database name to create
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Persist data between restarts
    ports:
      - "5432:5432"                     # Expose PostgreSQL port to host
    healthcheck:                        # Health check for dependency ordering
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s                     # Check every 10 seconds
      timeout: 5s                       # Timeout after 5 seconds
      retries: 5                        # Fail after 5 retries

  # ═══════════════════════════════════════════════════════════════
  # REDIS SERVICE
  # ═══════════════════════════════════════════════════════════════
  redis:
    image: redis:7-alpine              # Official Redis image
    container_name: admin_panel_redis
    restart: unless-stopped
    ports:
      - "6379:6379"                     # Expose Redis port
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ═══════════════════════════════════════════════════════════════
  # API SERVICE (FastAPI Backend)
  # ═══════════════════════════════════════════════════════════════
  api:
    build:
      context: ./apps/api              # Build from apps/api directory
      dockerfile: Dockerfile           # Use Dockerfile in that directory
    container_name: admin_panel_api
    restart: unless-stopped
    environment:
      - ENVIRONMENT=development        # Development mode
      - DEBUG=true                     # Enable debug logging
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/admin_panel
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=dev-secret-key-change-in-production-please
      - CORS_ORIGINS=["http://localhost:5173","http://localhost:3000","http://localhost"]
    ports:
      - "8000:8000"                     # Expose API port
    depends_on:
      db:
        condition: service_healthy     # Wait for DB to be healthy
      redis:
        condition: service_healthy     # Wait for Redis to be healthy
    volumes:
      - ./apps/api:/app                # Mount source for hot reload
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # ═══════════════════════════════════════════════════════════════
  # WEB SERVICE (React Frontend via Nginx)
  # ═══════════════════════════════════════════════════════════════
  web:
    build:
      context: ./apps/web
      dockerfile: Dockerfile
    container_name: admin_panel_web
    restart: unless-stopped
    ports:
      - "80:80"                         # Expose on standard HTTP port
    depends_on:
      - api                             # Start after API is up

# Named volume for database persistence
volumes:
  postgres_data:
```

## Backend Dockerfile Explained

```dockerfile
# ═══════════════════════════════════════════════════════════════
# STAGE 1: Builder
# ═══════════════════════════════════════════════════════════════
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \          # Compiler tools
    libpq-dev \                # PostgreSQL development files
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# ═══════════════════════════════════════════════════════════════
# STAGE 2: Production
# ═══════════════════════════════════════════════════════════════
FROM python:3.12-slim

# Create non-root user for security
RUN useradd --create-home appuser

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \                   # PostgreSQL client library
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Frontend Dockerfile Explained

```dockerfile
# ═══════════════════════════════════════════════════════════════
# STAGE 1: Build React App
# ═══════════════════════════════════════════════════════════════
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build production bundle
RUN npm run build

# ═══════════════════════════════════════════════════════════════
# STAGE 2: Serve with Nginx
# ═══════════════════════════════════════════════════════════════
FROM nginx:alpine

# Copy built files to Nginx serve directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
```

## Nginx Configuration Explained

```nginx
server {
    listen 80;                         # Listen on port 80
    server_name localhost;             # Server name
    root /usr/share/nginx/html;        # Document root
    index index.html;                  # Default file

    # API proxy - forwards /api requests to FastAPI
    location /api {
        proxy_pass http://api:8000;    # Forward to API service
        proxy_http_version 1.1;        # Use HTTP/1.1 for keepalive
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Serve static files and handle SPA routing
    location / {
        try_files $uri $uri/ /index.html;  # Fallback to index.html for SPA
    }

    # Gzip compression for better performance
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
```

---

# 5. Backend - Complete Reference

## 5.1 Entry Point: `app/main.py`

```python
"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.core.middleware import setup_middleware
from app.schemas.common import HealthResponse

# Initialize structured logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    This runs code:
    - BEFORE the app starts accepting requests (startup)
    - AFTER the app stops accepting requests (shutdown)
    
    Use for:
    - Database connection pools
    - Cache connections
    - Background task cleanup
    """
    # STARTUP
    logger.info(
        "application_startup",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )
    
    yield  # App runs here
    
    # SHUTDOWN
    logger.info("application_shutdown")


def create_application() -> FastAPI:
    """
    Application factory pattern.
    
    Why use a factory?
    - Testability: Create fresh instances for testing
    - Configuration: Different configs for different environments
    - Modularity: Clear initialization sequence
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Production-ready Admin Panel API",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",  # /api/v1/openapi.json
        docs_url=f"{settings.API_V1_PREFIX}/docs",              # /api/v1/docs
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",            # /api/v1/redoc
        lifespan=lifespan,
    )
    
    # ═══ CORS Middleware ═══
    # Allows frontend (different origin) to call API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,  # Allowed frontend URLs
        allow_credentials=True,                # Allow cookies
        allow_methods=["*"],                   # Allow all HTTP methods
        allow_headers=["*"],                   # Allow all headers
    )
    
    # ═══ Custom Middleware ═══
    # Request ID, logging, error handling
    setup_middleware(app)
    
    # ═══ API Routes ═══
    # All routes under /api/v1
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    # ═══ Health Check ═══
    # Root-level health endpoint (no auth required)
    @app.get("/health", response_model=HealthResponse, tags=["Health"])
    async def health_check():
        """Health check endpoint for load balancers and monitoring."""
        return HealthResponse(
            status="healthy",
            version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT,
        )
    
    return app


# Create the application instance
app = create_application()


# Allow running directly with: python -m app.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
```

## 5.2 Configuration: `app/core/config.py`

```python
"""Application configuration using Pydantic settings."""
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Pydantic Settings automatically:
    - Reads from environment variables
    - Reads from .env file
    - Validates types
    - Provides defaults
    
    Environment variable names match attribute names (case-insensitive).
    """
    
    # ═══ Application Settings ═══
    APP_NAME: str = "Admin Panel API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False
    
    # ═══ API Settings ═══
    API_V1_PREFIX: str = "/api/v1"
    
    # ═══ Security Settings ═══
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30      # 30 minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7         # 7 days
    ALGORITHM: str = "HS256"                    # JWT signing algorithm
    
    # ═══ Database Settings ═══
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/admin_panel"
    DATABASE_POOL_SIZE: int = 5                # Connection pool size
    DATABASE_MAX_OVERFLOW: int = 10            # Extra connections allowed
    
    # ═══ Redis Settings ═══
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ═══ CORS Settings ═══
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # ═══ Pagination Settings ═══
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"          # Load from .env file
        case_sensitive = True       # Match exact case


@lru_cache  # Cache the settings instance (singleton pattern)
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
```

## 5.3 Database: `app/core/database.py`

```python
"""Database configuration and session management."""
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


# ═══ Create Async Engine ═══
# The engine manages the connection pool
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,      # Number of connections to keep
    max_overflow=settings.DATABASE_MAX_OVERFLOW, # Extra connections when busy
    echo=settings.DEBUG,                         # Log SQL queries in debug mode
)


# ═══ Session Factory ═══
# Creates new database sessions
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,    # Don't expire objects after commit
    autocommit=False,          # Manual transaction control
    autoflush=False,           # Manual flush control
)


# ═══ Base Model Class ═══
# All models inherit from this
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# ═══ Database Session Dependency ═══
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a database session.
    
    Usage in endpoints:
        @router.get("/")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    
    Behavior:
    - Creates new session for each request
    - Auto-commits on success
    - Auto-rollbacks on exception
    - Always closes session
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

## 5.4 Security: `app/core/security.py`

```python
"""Security utilities for authentication and authorization."""
from datetime import datetime, timedelta, timezone
from typing import Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings


# ═══ Password Hashing ═══
# Using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: The password the user entered
        hashed_password: The stored hash from database
    
    Returns:
        True if password matches, False otherwise
    
    How bcrypt works:
    - Hash includes salt (random bytes)
    - Same password = different hash each time
    - Verification extracts salt and re-hashes
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storage.
    
    Args:
        password: Plain text password
    
    Returns:
        Bcrypt hash string (includes salt)
    
    Example output:
        $2b$12$LQv3c1yqBWVHxkd0LHAkCO...
        │  │  │
        │  │  └── Salt + Hash
        │  └── Cost factor (2^12 iterations)
        └── Algorithm identifier
    """
    return pwd_context.hash(password)


def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: Usually the user ID
        expires_delta: Custom expiration time (optional)
    
    Returns:
        Encoded JWT string
    
    Token payload structure:
    {
        "sub": "1",           # Subject (user ID)
        "exp": 1705123456,    # Expiration timestamp
        "type": "access"      # Token type
    }
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access"
    }
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: str | Any) -> str:
    """
    Create a JWT refresh token.
    
    Refresh tokens:
    - Live longer (7 days vs 30 minutes)
    - Used only to get new access tokens
    - Should be stored securely
    """
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh"
    }
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict[str, Any] | None:
    """
    Decode and validate a JWT token.
    
    Args:
        token: The JWT string
    
    Returns:
        Decoded payload dict, or None if invalid
    
    Validation includes:
    - Signature verification (using SECRET_KEY)
    - Expiration check
    - Algorithm check
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
```

## 5.5 Middleware: `app/core/middleware.py`

```python
"""Custom middleware for request processing."""
import time
import uuid
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger, bind_request_context

logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Adds a unique request ID to every request.
    
    Purpose:
    - Trace requests through logs
    - Correlate frontend errors with backend logs
    - Debug distributed systems
    
    The ID is:
    - Generated for each request
    - Added to request.state
    - Included in response headers
    - Logged with every log message
    """
    
    async def dispatch(self, request: Request, call_next):
        # Generate unique ID
        request_id = str(uuid.uuid4())
        
        # Store in request state (accessible in endpoints)
        request.state.request_id = request_id
        
        # Bind to logging context
        bind_request_context(request_id=request_id)
        
        # Process request
        response = await call_next(request)
        
        # Add to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every request with timing information.
    
    Logs include:
    - HTTP method (GET, POST, etc.)
    - Path (/api/v1/users)
    - Status code (200, 404, 500)
    - Duration in milliseconds
    - Client IP address
    - Request ID (from RequestIDMiddleware)
    """
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Log request completion
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            client_ip=request.client.host if request.client else None,
            request_id=getattr(request.state, "request_id", None),
        )
        
        return response


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled errors.
    
    Catches any exception not handled elsewhere and:
    - Logs the full error with traceback
    - Returns a generic 500 error to the client
    - Hides internal details from users
    """
    request_id = getattr(request.state, "request_id", None)
    
    logger.error(
        "unhandled_exception",
        error=str(exc),
        error_type=type(exc).__name__,
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "request_id": request_id,
        },
    )


def setup_middleware(app: FastAPI) -> None:
    """
    Configure all middleware for the application.
    
    Order matters! Middleware executes in reverse order:
    - Last added = first to process request
    - First added = last to process request
    """
    # Add exception handler
    app.add_exception_handler(Exception, global_exception_handler)
    
    # Add logging middleware (processes after request ID is set)
    app.add_middleware(RequestLoggingMiddleware)
    
    # Add request ID middleware (runs first)
    app.add_middleware(RequestIDMiddleware)
```

## 5.6 Dependencies: `app/api/deps.py`

```python
"""API dependencies for authentication and authorization."""
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User, UserRole
from app.services.user_service import UserService


# ═══ Security Scheme ═══
# Tells FastAPI to expect "Authorization: Bearer <token>" header
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    Get the current authenticated user from JWT token.
    
    This dependency:
    1. Extracts Bearer token from Authorization header
    2. Decodes and validates the JWT
    3. Loads the user from database
    4. Checks user is active
    
    Usage:
        @router.get("/me")
        async def get_me(user: User = Depends(get_current_user)):
            return user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode JWT token
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise credentials_exception
    
    # Verify it's an access token (not refresh)
    if payload.get("type") != "access":
        raise credentials_exception
    
    # Extract user ID
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Load user from database
    user_service = UserService(db)
    user = await user_service.get_by_id(int(user_id))
    
    if user is None:
        raise credentials_exception
    
    # Check user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Alias for get_current_user (kept for compatibility)."""
    return current_user


def require_role(*allowed_roles: UserRole):
    """
    Dependency factory for role-based access control.
    
    Creates a dependency that checks if user has required role.
    
    Usage:
        @router.post("/")
        async def create_user(
            user: User = Depends(require_role(UserRole.admin))
        ):
            ...
    """
    async def role_checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}",
            )
        return current_user
    return role_checker


# ═══ Pre-built Role Dependencies ═══
# Use these in endpoint signatures for cleaner code

AdminOnly = Depends(require_role(UserRole.admin))
"""Only admin users can access."""

AdminOrManager = Depends(require_role(UserRole.admin, UserRole.manager))
"""Admin or manager users can access."""

AnyRole = Depends(require_role(UserRole.admin, UserRole.manager, UserRole.viewer))
"""Any authenticated user can access."""


def get_request_info(request: Request) -> dict:
    """
    Extract request metadata for audit logging.
    
    Returns dict with:
    - ip_address: Client IP
    - user_agent: Browser/client info
    - request_id: Unique request identifier
    """
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "request_id": request.state.request_id if hasattr(request.state, "request_id") else None,
    }


# ═══ Type Aliases ═══
# Makes endpoint signatures cleaner

CurrentUser = Annotated[User, Depends(get_current_user)]
"""Injected current authenticated user."""

DbSession = Annotated[AsyncSession, Depends(get_db)]
"""Injected database session."""

RequestInfo = Annotated[dict, Depends(get_request_info)]
"""Injected request metadata for audit logs."""
```

## 5.7 Models - User: `app/models/user.py`

```python
"""User model with RBAC roles."""
import enum
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class UserRole(str, enum.Enum):
    """
    User roles for Role-Based Access Control (RBAC).
    
    Inherits from str for JSON serialization.
    """
    admin = "admin"       # Full system access
    manager = "manager"   # Can manage own resources
    viewer = "viewer"     # Read-only access


class User(Base):
    """
    User model for authentication and authorization.
    
    This is the central model for the auth system.
    """
    
    __tablename__ = "users"  # Database table name
    
    # ═══ Primary Key ═══
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # ═══ Authentication Fields ═══
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,      # No duplicate emails
        index=True,       # Fast lookups by email
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    # ═══ Profile Fields ═══
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # ═══ Authorization Fields ═══
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, values_callable=lambda x: [e.value for e in x]),
        default=UserRole.viewer,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,      # New users are active by default
        nullable=False
    )
    
    # ═══ Timestamp Fields ═══
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # Database sets this
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),        # Auto-update on changes
        nullable=False
    )
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True               # Null until first login
    )
    
    # ═══ Relationships ═══
    projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="owner",
        lazy="selectin"             # Eager load with SELECT IN
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"


# Imports at bottom to avoid circular imports
from app.models.project import Project
from app.models.audit_log import AuditLog
```

## 5.8 Services - User Service: `app/services/user_service.py`

```python
"""User service for business logic."""
from datetime import datetime, timezone
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """
    Service layer for user operations.
    
    Why use a service layer?
    - Separates business logic from HTTP handling
    - Reusable across different endpoints
    - Easier to test
    - Cleaner endpoint code
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_list(
        self,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        search: str | None = None,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[User], int]:
        """
        Get paginated list of users with filters.
        
        Returns:
            Tuple of (users list, total count)
        """
        # Build base queries
        query = select(User)
        count_query = select(func.count(User.id))
        
        # ═══ Apply Filters ═══
        
        # Search filter (email or name)
        if search:
            search_filter = f"%{search}%"
            query = query.where(
                (User.email.ilike(search_filter)) |
                (User.full_name.ilike(search_filter))
            )
            count_query = count_query.where(
                (User.email.ilike(search_filter)) |
                (User.full_name.ilike(search_filter))
            )
        
        # Role filter
        if role:
            query = query.where(User.role == role)
            count_query = count_query.where(User.role == role)
        
        # Active status filter
        if is_active is not None:
            query = query.where(User.is_active == is_active)
            count_query = count_query.where(User.is_active == is_active)
        
        # ═══ Apply Sorting ═══
        sort_column = getattr(User, sort_by, User.created_at)
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # ═══ Apply Pagination ═══
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # ═══ Execute Queries ═══
        result = await self.db.execute(query)
        count_result = await self.db.execute(count_query)
        
        return list(result.scalars().all()), count_result.scalar_one()
    
    async def create(self, data: UserCreate) -> User:
        """Create a new user."""
        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=get_password_hash(data.password),
            role=data.role,
        )
        self.db.add(user)
        await self.db.flush()        # Send to DB, get ID
        await self.db.refresh(user)  # Reload with DB-generated values
        return user
    
    async def update(self, user: User, data: UserUpdate) -> User:
        """Update a user."""
        update_data = data.model_dump(exclude_unset=True)  # Only changed fields
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def update_password(self, user: User, new_password: str) -> User:
        """Update user password."""
        user.hashed_password = get_password_hash(new_password)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def update_last_login(self, user: User) -> User:
        """Update last login timestamp."""
        user.last_login = datetime.now(timezone.utc)
        await self.db.flush()
        return user
    
    async def delete(self, user: User) -> None:
        """Delete a user."""
        await self.db.delete(user)
        await self.db.flush()
    
    async def authenticate(self, email: str, password: str) -> User | None:
        """
        Authenticate user by email and password.
        
        Returns:
            User if credentials valid, None otherwise
        """
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user
    
    async def count(self) -> int:
        """Get total user count."""
        result = await self.db.execute(select(func.count(User.id)))
        return result.scalar_one()
```

## 5.9 Endpoints - Auth: `app/api/v1/endpoints/auth.py`

```python
"""Authentication endpoints."""
from fastapi import APIRouter, HTTPException, status
from app.api.deps import CurrentUser, DbSession, RequestInfo
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.models.audit_log import AuditAction
from app.schemas.auth import AuthResponse, LoginRequest, RefreshTokenRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.audit_service import AuditService
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=AuthResponse)
async def login(
    data: LoginRequest,
    db: DbSession,
    request_info: RequestInfo,
):
    """
    Authenticate user and return tokens.
    
    Request body:
        {
            "email": "admin@example.com",
            "password": "admin123"
        }
    
    Response:
        {
            "user": {...},
            "tokens": {
                "access_token": "eyJ...",
                "refresh_token": "eyJ..."
            }
        }
    """
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    # Authenticate user
    user = await user_service.authenticate(data.email, data.password)
    
    if not user:
        # Log failed attempt
        await audit_service.log(
            action=AuditAction.login_failed,
            resource_type="auth",
            details={"email": data.email},
            **request_info,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Update last login
    await user_service.update_last_login(user)
    
    # Log successful login
    await audit_service.log(
        action=AuditAction.login,
        resource_type="auth",
        user_id=user.id,
        **request_info,
    )
    
    # Refresh user to get updated fields
    await db.refresh(user)
    
    # Create tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        ),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest, db: DbSession):
    """
    Refresh access token using refresh token.
    
    Use this when access token expires (401 error).
    """
    payload = decode_token(data.refresh_token)
    
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # Verify user still exists and is active
    user_service = UserService(db)
    user = await user_service.get_by_id(int(user_id))
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    # Create new tokens
    access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
    )


@router.post("/logout")
async def logout(
    current_user: CurrentUser,
    db: DbSession,
    request_info: RequestInfo,
):
    """
    Logout user.
    
    Note: With JWTs, we can't truly invalidate tokens.
    This endpoint logs the action for audit purposes.
    
    For true logout, implement token blacklisting with Redis.
    """
    audit_service = AuditService(db)
    
    await audit_service.log(
        action=AuditAction.logout,
        resource_type="auth",
        user_id=current_user.id,
        **request_info,
    )
    
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser):
    """
    Get current user information.
    
    Useful for:
    - Verifying token is valid
    - Getting updated user data
    - Checking user role
    """
    return UserResponse.model_validate(current_user)
```

---

# 6. Frontend - Complete Reference

## 6.1 Entry Point: `src/main.tsx`

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from '@/contexts/auth-context'
import { ThemeProvider } from '@/contexts/theme-context'
import { AppLayout } from '@/components/layout/app-layout'
import { Toaster } from '@/components/layout/toaster'
import { LoginPage } from '@/pages/login'
import { DashboardPage } from '@/pages/dashboard'
import { ProjectsPage } from '@/pages/projects'
import { UsersPage } from '@/pages/users'
import { AuditLogsPage } from '@/pages/audit-logs'
import { SettingsPage } from '@/pages/settings'
import './index.css'

// ═══ React Query Configuration ═══
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,    // Data is fresh for 5 minutes
      retry: 1,                     // Retry failed requests once
      refetchOnWindowFocus: false,  // Don't refetch when tab gains focus
    },
  },
})

// ═══ App Render ═══
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {/* React Query - Server state management */}
    <QueryClientProvider client={queryClient}>
      {/* Theme - Dark/light mode */}
      <ThemeProvider>
        {/* Auth - User authentication state */}
        <AuthProvider>
          {/* Router - Client-side navigation */}
          <BrowserRouter>
            <Routes>
              {/* Public route - no auth required */}
              <Route path="/login" element={<LoginPage />} />
              
              {/* Protected routes - wrapped in AppLayout */}
              <Route element={<AppLayout />}>
                <Route path="/" element={<DashboardPage />} />
                <Route path="/projects" element={<ProjectsPage />} />
                <Route path="/users" element={<UsersPage />} />
                <Route path="/audit-logs" element={<AuditLogsPage />} />
                <Route path="/settings" element={<SettingsPage />} />
              </Route>
            </Routes>
          </BrowserRouter>
          
          {/* Toast notifications */}
          <Toaster />
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  </React.StrictMode>
)
```

## 6.2 Auth Context: `src/contexts/auth-context.tsx`

```tsx
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { api } from '@/lib/api'
import type { User, AuthResponse } from '@/lib/types'

// ═══ Context Type Definition ═══
interface AuthContextType {
  user: User | null               // Current user or null if not logged in
  isLoading: boolean              // True during initial auth check
  isAuthenticated: boolean        // Convenience boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}

// ═══ Create Context ═══
const AuthContext = createContext<AuthContextType | null>(null)

// ═══ Provider Component ═══
export function AuthProvider({ children }: { children: React.ReactNode }) {
  // Initialize user from localStorage (persists across page reloads)
  const [user, setUser] = useState<User | null>(() => {
    const stored = localStorage.getItem('user')
    return stored ? JSON.parse(stored) : null
  })
  const [isLoading, setIsLoading] = useState(true)

  // ═══ Refresh User Data ═══
  const refreshUser = useCallback(async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      setUser(null)
      setIsLoading(false)
      return
    }

    try {
      // Verify token is still valid
      const userData = await api.get<User>('/auth/me')
      setUser(userData)
      localStorage.setItem('user', JSON.stringify(userData))
    } catch {
      // Token invalid, clear auth state
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }, [])

  // ═══ Initial Auth Check ═══
  useEffect(() => {
    refreshUser()
  }, [refreshUser])

  // ═══ Login Function ═══
  const login = async (email: string, password: string) => {
    const response = await api.post<AuthResponse>('/auth/login', { email, password })
    
    // Store tokens
    localStorage.setItem('access_token', response.tokens.access_token)
    localStorage.setItem('refresh_token', response.tokens.refresh_token)
    localStorage.setItem('user', JSON.stringify(response.user))
    
    // Update state
    setUser(response.user)
  }

  // ═══ Logout Function ═══
  const logout = async () => {
    try {
      await api.post('/auth/logout')
    } catch {
      // Ignore errors - we're logging out anyway
    } finally {
      // Clear everything
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

// ═══ Custom Hook ═══
export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
```

## 6.3 API Client: `src/lib/api.ts`

```tsx
const API_BASE = '/api/v1'

type QueryParams = Record<string, string | number | boolean | undefined | null>

interface RequestOptions extends RequestInit {
  params?: QueryParams
}

// ═══ Custom Error Class ═══
class ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    public data?: unknown
  ) {
    super(`API Error: ${status} ${statusText}`)
    this.name = 'ApiError'
  }
}

// ═══ Core Request Function ═══
async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { params, ...init } = options
  
  // Build URL with query parameters
  let url = `${API_BASE}${endpoint}`
  if (params) {
    const searchParams = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        searchParams.append(key, String(value))
      }
    })
    const queryString = searchParams.toString()
    if (queryString) {
      url += `?${queryString}`
    }
  }
  
  // Get auth token from localStorage
  const token = localStorage.getItem('access_token')
  
  // Setup headers
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...init.headers,
  }
  
  // Add auth header if token exists
  if (token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
  }
  
  // Make request
  const response = await fetch(url, {
    ...init,
    headers,
  })
  
  // Handle 401 - Token expired or invalid
  if (response.status === 401) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    window.location.href = '/login'
    throw new ApiError(401, 'Unauthorized')
  }
  
  // Handle other errors
  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new ApiError(response.status, response.statusText, data)
  }
  
  // Handle empty responses
  const text = await response.text()
  if (!text) return {} as T
  
  return JSON.parse(text)
}

// ═══ Exported API Methods ═══
export const api = {
  get: <T>(endpoint: string, params?: QueryParams) =>
    request<T>(endpoint, { method: 'GET', params }),
    
  post: <T>(endpoint: string, data?: unknown) =>
    request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    }),
    
  patch: <T>(endpoint: string, data?: unknown) =>
    request<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    }),
    
  delete: <T>(endpoint: string) =>
    request<T>(endpoint, { method: 'DELETE' }),
}

export { ApiError }
```

## 6.4 Type Definitions: `src/lib/types.ts`

```tsx
// ═══ User Types ═══
export type UserRole = 'admin' | 'manager' | 'viewer'

export interface User {
  id: number
  email: string
  full_name: string
  role: UserRole
  is_active: boolean
  created_at: string
  updated_at: string
  last_login: string | null
}

export interface UserCreate {
  email: string
  full_name: string
  password: string
  role: UserRole
}

export interface UserUpdate {
  email?: string
  full_name?: string
  role?: UserRole
  is_active?: boolean
}

// ═══ Project Types ═══
export type ProjectStatus = 'draft' | 'active' | 'on_hold' | 'completed' | 'archived'
export type ProjectPriority = 'low' | 'medium' | 'high' | 'critical'

export interface Project {
  id: number
  name: string
  description: string | null
  status: ProjectStatus
  priority: ProjectPriority
  budget: number | null
  start_date: string | null
  end_date: string | null
  owner_id: number
  owner: User
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  name: string
  description?: string
  status?: ProjectStatus
  priority?: ProjectPriority
  budget?: number
  start_date?: string
  end_date?: string
}

export interface ProjectUpdate {
  name?: string
  description?: string
  status?: ProjectStatus
  priority?: ProjectPriority
  budget?: number
  start_date?: string
  end_date?: string
}

// ═══ Audit Log Types ═══
export type AuditAction =
  | 'login'
  | 'logout'
  | 'login_failed'
  | 'user_create'
  | 'user_update'
  | 'user_delete'
  | 'user_role_change'
  | 'password_change'
  | 'project_create'
  | 'project_update'
  | 'project_delete'
  | 'project_status_change'

export interface AuditLog {
  id: number
  user_id: number | null
  user_email: string | null
  action: AuditAction
  resource_type: string
  resource_id: number | null
  details: Record<string, unknown> | null
  ip_address: string | null
  user_agent: string | null
  request_id: string | null
  created_at: string
}

// ═══ Auth Types ═══
export interface TokenResponse {
  access_token: string
  refresh_token: string
}

export interface AuthResponse {
  user: User
  tokens: TokenResponse
}

// ═══ API Response Types ═══
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface StatsResponse {
  total_users: number
  total_projects: number
  active_projects: number
  recent_activity_count: number
}

// ═══ Pagination Params ═══
export interface PaginationParams {
  page?: number
  page_size?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
  search?: string
  [key: string]: string | number | boolean | undefined | null
}
```

---

# 7. Database - Complete Reference

## 7.1 Schema Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                  users                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ id                 │ SERIAL         │ PRIMARY KEY                           │
│ email              │ VARCHAR(255)   │ UNIQUE, NOT NULL, INDEX               │
│ hashed_password    │ VARCHAR(255)   │ NOT NULL                              │
│ full_name          │ VARCHAR(255)   │ NOT NULL                              │
│ role               │ userrole       │ NOT NULL, DEFAULT 'viewer'            │
│ is_active          │ BOOLEAN        │ NOT NULL, DEFAULT true                │
│ created_at         │ TIMESTAMPTZ    │ NOT NULL, DEFAULT now()               │
│ updated_at         │ TIMESTAMPTZ    │ NOT NULL, DEFAULT now()               │
│ last_login         │ TIMESTAMPTZ    │ NULL                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ 1:N (owner_id)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                projects                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ id                 │ SERIAL         │ PRIMARY KEY                           │
│ name               │ VARCHAR(255)   │ NOT NULL, INDEX                       │
│ description        │ TEXT           │ NULL                                  │
│ status             │ projectstatus  │ NOT NULL, DEFAULT 'draft'             │
│ priority           │ projectpriority│ NOT NULL, DEFAULT 'medium'            │
│ budget             │ INTEGER        │ NULL (stored in cents)                │
│ start_date         │ TIMESTAMPTZ    │ NULL                                  │
│ end_date           │ TIMESTAMPTZ    │ NULL                                  │
│ owner_id           │ INTEGER        │ NOT NULL, FOREIGN KEY → users(id)     │
│ created_at         │ TIMESTAMPTZ    │ NOT NULL, DEFAULT now()               │
│ updated_at         │ TIMESTAMPTZ    │ NOT NULL, DEFAULT now()               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              audit_logs                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ id                 │ SERIAL         │ PRIMARY KEY                           │
│ user_id            │ INTEGER        │ NULL, FOREIGN KEY → users(id)         │
│ action             │ auditaction    │ NOT NULL, INDEX                       │
│ resource_type      │ VARCHAR(50)    │ NOT NULL, INDEX                       │
│ resource_id        │ INTEGER        │ NULL                                  │
│ details            │ JSONB          │ NULL                                  │
│ ip_address         │ VARCHAR(45)    │ NULL                                  │
│ user_agent         │ TEXT           │ NULL                                  │
│ request_id         │ VARCHAR(36)    │ NULL, INDEX                           │
│ created_at         │ TIMESTAMPTZ    │ NOT NULL, DEFAULT now(), INDEX        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 7.2 PostgreSQL Enums

```sql
-- User roles
CREATE TYPE userrole AS ENUM ('admin', 'manager', 'viewer');

-- Project status
CREATE TYPE projectstatus AS ENUM ('draft', 'active', 'on_hold', 'completed', 'archived');

-- Project priority
CREATE TYPE projectpriority AS ENUM ('low', 'medium', 'high', 'critical');

-- Audit actions
CREATE TYPE auditaction AS ENUM (
    'login', 'logout', 'login_failed',
    'user_create', 'user_update', 'user_delete', 'user_role_change',
    'password_change',
    'project_create', 'project_update', 'project_delete', 'project_status_change'
);
```

## 7.3 Alembic Migrations

```python
# alembic/versions/001_initial.py
"""Initial migration - create all tables"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create enum types
    op.execute("CREATE TYPE userrole AS ENUM ('admin', 'manager', 'viewer')")
    op.execute("CREATE TYPE projectstatus AS ENUM ('draft', 'active', 'on_hold', 'completed', 'archived')")
    op.execute("CREATE TYPE projectpriority AS ENUM ('low', 'medium', 'high', 'critical')")
    op.execute("""
        CREATE TYPE auditaction AS ENUM (
            'login', 'logout', 'login_failed',
            'user_create', 'user_update', 'user_delete', 'user_role_change',
            'password_change',
            'project_create', 'project_update', 'project_delete', 'project_status_change'
        )
    """)
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('role', postgresql.ENUM('admin', 'manager', 'viewer', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'])
    
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', postgresql.ENUM('draft', 'active', 'on_hold', 'completed', 'archived', name='projectstatus'), nullable=False),
        sa.Column('priority', postgresql.ENUM('low', 'medium', 'high', 'critical', name='projectpriority'), nullable=False),
        sa.Column('budget', sa.Integer(), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_projects_name', 'projects', ['name'])
    op.create_index('ix_projects_owner_id', 'projects', ['owner_id'])
    
    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', postgresql.ENUM(name='auditaction'), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=True),
        sa.Column('details', postgresql.JSONB(), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('request_id', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('ix_audit_logs_resource_type', 'audit_logs', ['resource_type'])
    op.create_index('ix_audit_logs_request_id', 'audit_logs', ['request_id'])
    op.create_index('ix_audit_logs_created_at', 'audit_logs', ['created_at'])
    op.create_index('ix_audit_logs_user_id', 'audit_logs', ['user_id'])


def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('projects')
    op.drop_table('users')
    op.execute('DROP TYPE auditaction')
    op.execute('DROP TYPE projectpriority')
    op.execute('DROP TYPE projectstatus')
    op.execute('DROP TYPE userrole')
```

---

# 8-20: Additional Sections

Due to the extensive length, the remaining sections are summarized below. Each would follow the same detailed pattern:

## 8. Authentication System
- JWT token structure
- Token lifecycle
- Password hashing algorithm
- Session management
- Token refresh flow

## 9. Authorization (RBAC) System  
- Role definitions
- Permission matrix
- Implementation details
- Frontend role checks

## 10. API Reference
- Complete endpoint documentation
- Request/response examples
- Error codes

## 11. Error Handling
- Backend error handling
- Frontend error handling
- Error response format

## 12. Logging & Observability
- Structured logging format
- Request ID tracing
- Log levels
- Monitoring recommendations

## 13. Security Considerations
- Authentication security
- Input validation
- SQL injection prevention
- XSS prevention
- CORS configuration
- Rate limiting

## 14. Performance Optimizations
- Database query optimization
- Connection pooling
- Frontend caching
- Code splitting

## 15. Testing Guide
- Backend testing with pytest
- Frontend testing with Vitest
- E2E testing with Playwright

## 16. Deployment - Complete Guide
- Production checklist
- Environment configuration
- SSL/TLS setup
- Monitoring setup

## 17. Maintenance & Operations
- Backup procedures
- Update procedures
- Scaling considerations

## 18. Extending the Project
- Adding new models
- Adding new endpoints
- Adding new pages
- Adding new features

## 19. Troubleshooting Encyclopedia
- Common errors and solutions
- Debug procedures
- Log analysis

## 20. Glossary
- Technical terms defined
- Acronyms explained

---

# Quick Reference Cards

## Commands Cheat Sheet

```bash
# ═══ Docker Commands ═══
docker-compose up -d                    # Start all services
docker-compose down                     # Stop all services
docker-compose down -v                  # Stop and delete data
docker-compose logs -f api              # View API logs
docker-compose exec api bash            # Shell into API container
docker-compose restart api              # Restart API

# ═══ Database Commands ═══
docker-compose exec api alembic upgrade head      # Run migrations
docker-compose exec api alembic downgrade -1      # Rollback one
docker-compose exec api python seed_db.py         # Seed data
docker-compose exec db psql -U postgres -d admin_panel  # DB shell

# ═══ Useful Queries ═══
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 10;
```

## Environment Variables

```bash
# Required
SECRET_KEY=your-32-char-secret-key

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname

# Optional
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=["https://your-frontend.com"]
```

## Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | admin123 |
| Manager | manager@example.com | manager123 |
| Viewer | viewer@example.com | viewer123 |

---

**End of Technical Reference**

*Last updated: January 2026*
