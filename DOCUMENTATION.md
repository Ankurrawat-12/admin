# Admin Panel - Complete Technical Documentation

A production-ready full-stack admin panel with FastAPI backend and React frontend.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Authentication Flow](#authentication-flow)
4. [Data Flow Examples](#data-flow-examples)
5. [Backend Structure](#backend-structure)
6. [Frontend Structure](#frontend-structure)
7. [Database Models](#database-models)
8. [API Endpoints](#api-endpoints)
9. [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
10. [Running Locally](#running-locally)
11. [Deployment Guide](#deployment-guide)
12. [Environment Variables](#environment-variables)
13. [Troubleshooting](#troubleshooting)

---

## Overview

### Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Vite, TypeScript, TailwindCSS, shadcn/ui, React Query, React Router |
| **Backend** | Python 3.12, FastAPI, SQLAlchemy (async), Pydantic, Alembic |
| **Database** | PostgreSQL 16 |
| **Cache** | Redis 7 |
| **Auth** | JWT (access + refresh tokens), bcrypt password hashing |
| **Infrastructure** | Docker, Docker Compose, Nginx |

### Demo Credentials

| Role | Email | Password | Permissions |
|------|-------|----------|-------------|
| **Admin** | admin@example.com | admin123 | Full access to everything |
| **Manager** | manager@example.com | manager123 | Create/edit own projects, view users |
| **Viewer** | viewer@example.com | viewer123 | Read-only access |

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USER'S BROWSER                                      │
│                                                                                  │
│  1. User visits http://localhost                                                │
│  2. Nginx serves React app (static files)                                       │
│  3. React app makes API calls to /api/*                                         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              NGINX (Port 80)                                     │
│                                                                                  │
│  location / {                                                                   │
│      # Serves React static files (index.html, JS, CSS)                         │
│  }                                                                              │
│                                                                                  │
│  location /api {                                                                │
│      proxy_pass http://api:8000;  # Forwards to FastAPI                        │
│  }                                                                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                      ┌─────────────────┴─────────────────┐
                      ▼                                   ▼
┌────────────────────────────────┐    ┌────────────────────────────────────────────┐
│     FASTAPI BACKEND            │    │         REACT FRONTEND                      │
│     (Port 8000)                │    │         (Served by Nginx)                   │
│                                │    │                                             │
│  ┌──────────────────────────┐ │    │  ┌─────────────────────────────────────┐   │
│  │  Middleware Layer        │ │    │  │  Pages                              │   │
│  │  • Request ID generation │ │    │  │  • Login                            │   │
│  │  • Request logging       │ │    │  │  • Dashboard                        │   │
│  │  • CORS handling         │ │    │  │  • Projects                         │   │
│  │  • Error handling        │ │    │  │  • Users                            │   │
│  └──────────────────────────┘ │    │  │  • Audit Logs                       │   │
│              │                │    │  │  • Settings                         │   │
│              ▼                │    │  └─────────────────────────────────────┘   │
│  ┌──────────────────────────┐ │    │                                             │
│  │  Auth Layer              │ │    │  ┌─────────────────────────────────────┐   │
│  │  • JWT validation        │ │    │  │  State Management                   │   │
│  │  • User extraction       │ │    │  │  • React Query (server state)       │   │
│  │  • Role checking (RBAC)  │ │    │  │  • Auth Context (user state)        │   │
│  └──────────────────────────┘ │    │  │  • Theme Context (dark/light)       │   │
│              │                │    │  └─────────────────────────────────────┘   │
│              ▼                │    │                                             │
│  ┌──────────────────────────┐ │    │  ┌─────────────────────────────────────┐   │
│  │  API Endpoints           │ │    │  │  API Client                         │   │
│  │  • /auth/*               │ │    │  │  • Auto-attaches JWT                │   │
│  │  • /users/*              │ │    │  │  • Handles 401 redirect             │   │
│  │  • /projects/*           │ │    │  │  • Type-safe requests               │   │
│  │  • /audit-logs/*         │ │    │  └─────────────────────────────────────┘   │
│  │  • /dashboard/*          │ │    │                                             │
│  └──────────────────────────┘ │    └────────────────────────────────────────────┘
│              │                │
│              ▼                │
│  ┌──────────────────────────┐ │
│  │  Services Layer          │ │
│  │  • Business logic        │ │
│  │  • Data validation       │ │
│  │  • Complex operations    │ │
│  └──────────────────────────┘ │
│              │                │
│              ▼                │
│  ┌──────────────────────────┐ │
│  │  Data Layer              │ │
│  │  • SQLAlchemy models     │ │
│  │  • Async DB sessions     │ │
│  │  • Query building        │ │
│  └──────────────────────────┘ │
└────────────────────────────────┘
            │           │
            ▼           ▼
┌─────────────────┐  ┌─────────────────┐
│   POSTGRESQL    │  │     REDIS       │
│   (Port 5432)   │  │   (Port 6379)   │
│                 │  │                 │
│  Tables:        │  │  Uses:          │
│  • users        │  │  • Session cache│
│  • projects     │  │  • Rate limiting│
│  • audit_logs   │  │  • Job queues   │
└─────────────────┘  └─────────────────┘
```

### Docker Services

```yaml
services:
  db:       # PostgreSQL 16 - Data storage
  redis:    # Redis 7 - Caching & background jobs
  api:      # FastAPI - Backend API server
  web:      # Nginx - Serves frontend & proxies API
```

---

## Authentication Flow

### Login Process

```
┌─────────────────┐                                    ┌─────────────────┐
│    Browser      │                                    │    FastAPI      │
└────────┬────────┘                                    └────────┬────────┘
         │                                                      │
         │  1. POST /api/v1/auth/login                         │
         │     {email: "admin@example.com", password: "admin123"}
         │ ─────────────────────────────────────────────────────▶
         │                                                      │
         │                    2. Validate credentials           │
         │                       - Find user by email           │
         │                       - Verify bcrypt password       │
         │                       - Check user is active         │
         │                                                      │
         │                    3. Generate tokens                │
         │                       - Access token (30 min)        │
         │                       - Refresh token (7 days)       │
         │                                                      │
         │                    4. Create audit log               │
         │                       - action: "login"              │
         │                       - user_id, ip_address, etc.    │
         │                                                      │
         │  5. Response                                         │
         │     {user: {...}, tokens: {access_token, refresh_token}}
         │ ◀─────────────────────────────────────────────────────
         │                                                      │
         │  6. Store in localStorage                            │
         │     - access_token                                   │
         │     - refresh_token                                  │
         │     - user (JSON)                                    │
         │                                                      │
         │  7. Redirect to Dashboard                            │
         │                                                      │
```

### Authenticated Request

```
┌─────────────────┐                                    ┌─────────────────┐
│    Browser      │                                    │    FastAPI      │
└────────┬────────┘                                    └────────┬────────┘
         │                                                      │
         │  1. GET /api/v1/projects                             │
         │     Headers: Authorization: Bearer <access_token>    │
         │ ─────────────────────────────────────────────────────▶
         │                                                      │
         │                    2. Middleware                     │
         │                       - Extract Bearer token         │
         │                       - Decode JWT                   │
         │                       - Validate expiration          │
         │                       - Load user from DB            │
         │                       - Check role permissions       │
         │                                                      │
         │  3. Response (if authorized)                         │
         │     {items: [...], total: 10, page: 1}              │
         │ ◀─────────────────────────────────────────────────────
         │                                                      │
```

### Token Refresh

```
When access_token expires (after 30 minutes):

1. API returns 401 Unauthorized
2. Frontend uses refresh_token to get new tokens
3. POST /api/v1/auth/refresh {refresh_token: "..."}
4. Backend validates refresh_token, issues new pair
5. Frontend updates localStorage
6. Retry original request
```

---

## Data Flow Examples

### Creating a New Project

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: User Action                                                          │
│ User clicks "Create Project" button, fills form, clicks "Save"               │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: Frontend Validation                                                  │
│ React Hook Form + Zod validates:                                             │
│ - name: required, min 1 char                                                 │
│ - status: must be valid enum                                                 │
│ - priority: must be valid enum                                               │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: API Call                                                             │
│ useMutation calls: api.post('/projects', formData)                           │
│ Request includes Authorization header from localStorage                       │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: Nginx Proxy                                                          │
│ /api/v1/projects → http://api:8000/api/v1/projects                          │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: FastAPI Middleware                                                   │
│ a. RequestIDMiddleware: Generates UUID for request tracing                   │
│ b. RequestLoggingMiddleware: Logs method, path, duration                     │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 6: Dependency Injection                                                 │
│ a. HTTPBearer: Extracts JWT from Authorization header                        │
│ b. get_current_user: Decodes JWT, queries user from DB                       │
│ c. require_role(admin, manager): Verifies user has permission                │
│ d. get_db: Provides async database session                                   │
│ e. get_request_info: Extracts IP, user agent for audit log                   │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 7: Endpoint Handler (app/api/v1/endpoints/projects.py)                  │
│                                                                              │
│ @router.post("", response_model=ProjectResponse)                             │
│ async def create_project(                                                    │
│     data: ProjectCreate,           # Pydantic validates request body         │
│     db: DbSession,                 # Injected database session               │
│     current_user: User = AdminOrManager,  # Injected + role checked          │
│     request_info: RequestInfo = None,     # IP, user agent, request ID       │
│ ):                                                                           │
│     project_service = ProjectService(db)                                     │
│     project = await project_service.create(data, current_user.id)            │
│                                                                              │
│     await audit_service.log(                                                 │
│         action=AuditAction.project_create,                                   │
│         resource_type="project",                                             │
│         user_id=current_user.id,                                             │
│         resource_id=project.id,                                              │
│         details={"name": project.name},                                      │
│         **request_info,                                                      │
│     )                                                                        │
│                                                                              │
│     return ProjectResponse.model_validate(project)                           │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 8: Service Layer (app/services/project_service.py)                      │
│                                                                              │
│ async def create(self, data: ProjectCreate, owner_id: int) -> Project:       │
│     project = Project(                                                       │
│         name=data.name,                                                      │
│         description=data.description,                                        │
│         status=data.status,                                                  │
│         priority=data.priority,                                              │
│         owner_id=owner_id,                                                   │
│     )                                                                        │
│     self.db.add(project)                                                     │
│     await self.db.flush()      # Sends INSERT to database                    │
│     await self.db.refresh(project)  # Gets generated ID, timestamps          │
│     return project                                                           │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 9: Database                                                             │
│                                                                              │
│ INSERT INTO projects (name, description, status, priority, owner_id,         │
│                       created_at, updated_at)                                │
│ VALUES ('New Project', '...', 'active', 'high', 1, NOW(), NOW())            │
│ RETURNING id, created_at, updated_at;                                        │
│                                                                              │
│ INSERT INTO audit_logs (user_id, action, resource_type, resource_id, ...)    │
│ VALUES (1, 'project_create', 'project', 5, ...);                            │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 10: Response                                                            │
│                                                                              │
│ {                                                                            │
│   "id": 5,                                                                   │
│   "name": "New Project",                                                     │
│   "status": "active",                                                        │
│   "priority": "high",                                                        │
│   "owner": {"id": 1, "email": "admin@example.com", ...},                    │
│   "created_at": "2024-01-15T10:30:00Z",                                     │
│   ...                                                                        │
│ }                                                                            │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STEP 11: Frontend Updates                                                    │
│                                                                              │
│ a. React Query mutation onSuccess callback fires                             │
│ b. queryClient.invalidateQueries(['projects']) triggers refetch              │
│ c. Toast notification: "Project created successfully"                        │
│ d. Modal closes                                                              │
│ e. Project list automatically refreshes with new data                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Backend Structure

### Directory Layout

```
apps/api/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   │
│   ├── core/                      # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py              # Settings from environment
│   │   ├── database.py            # SQLAlchemy setup
│   │   ├── security.py            # JWT & password hashing
│   │   ├── logging.py             # Structured logging (structlog)
│   │   └── middleware.py          # Request ID, logging middleware
│   │
│   ├── api/                       # API layer
│   │   ├── __init__.py
│   │   ├── deps.py                # Dependencies (auth, DB, etc.)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py          # Combines all endpoint routers
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py        # Login, logout, refresh, me
│   │           ├── users.py       # User CRUD
│   │           ├── projects.py    # Project CRUD
│   │           ├── audit.py       # Audit log viewing
│   │           └── dashboard.py   # Dashboard stats
│   │
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py                # User model + UserRole enum
│   │   ├── project.py             # Project model + Status/Priority enums
│   │   └── audit_log.py           # AuditLog model + AuditAction enum
│   │
│   ├── schemas/                   # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── auth.py                # LoginRequest, AuthResponse, etc.
│   │   ├── user.py                # UserCreate, UserUpdate, UserResponse
│   │   ├── project.py             # ProjectCreate, ProjectResponse, etc.
│   │   ├── audit.py               # AuditLogResponse
│   │   └── common.py              # Pagination, health check, etc.
│   │
│   └── services/                  # Business logic layer
│       ├── __init__.py
│       ├── user_service.py        # User operations
│       ├── project_service.py     # Project operations
│       └── audit_service.py       # Audit logging operations
│
├── alembic/                       # Database migrations
│   ├── versions/                  # Migration files
│   ├── env.py                     # Alembic configuration
│   └── script.py.mako             # Migration template
│
├── alembic.ini                    # Alembic settings
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container build instructions
├── seed_db.py                     # Database seeding script
└── env.example                    # Example environment variables
```

### Key Files Explained

#### `app/main.py` - Application Factory

```python
def create_application() -> FastAPI:
    app = FastAPI(
        title="Admin Panel API",
        docs_url="/api/v1/docs",      # Swagger UI
        redoc_url="/api/v1/redoc",    # ReDoc
    )
    
    # 1. CORS middleware (allows frontend to call API)
    app.add_middleware(CORSMiddleware, ...)
    
    # 2. Custom middleware (request ID, logging)
    setup_middleware(app)
    
    # 3. Include all API routes
    app.include_router(api_router, prefix="/api/v1")
    
    # 4. Health check endpoint
    @app.get("/health")
    async def health_check(): ...
    
    return app
```

#### `app/core/config.py` - Configuration

```python
class Settings(BaseSettings):
    # Loaded from environment variables or .env file
    
    SECRET_KEY: str                    # For JWT signing (REQUIRED!)
    DATABASE_URL: str                  # PostgreSQL connection
    REDIS_URL: str                     # Redis connection
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30   # Short-lived
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7      # Long-lived
    
    CORS_ORIGINS: list[str]            # Allowed frontend URLs
    ENVIRONMENT: str = "development"   # dev/staging/production
```

#### `app/core/security.py` - Authentication

```python
# Password hashing (bcrypt)
def get_password_hash(password: str) -> str
def verify_password(plain_password: str, hashed_password: str) -> bool

# JWT tokens
def create_access_token(subject: str) -> str    # 30 min expiry
def create_refresh_token(subject: str) -> str   # 7 day expiry
def decode_token(token: str) -> dict | None     # Validates & decodes
```

#### `app/api/deps.py` - Dependency Injection

```python
# Database session
async def get_db() -> AsyncSession

# Current user from JWT
async def get_current_user(credentials, db) -> User

# Role checking factory
def require_role(*allowed_roles: UserRole)

# Pre-built role dependencies
AdminOnly = Depends(require_role(UserRole.admin))
AdminOrManager = Depends(require_role(UserRole.admin, UserRole.manager))

# Type aliases for clean endpoint signatures
CurrentUser = Annotated[User, Depends(get_current_user)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
```

#### `app/services/user_service.py` - Business Logic

```python
class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # CRUD operations
    async def get_by_id(user_id: int) -> User | None
    async def get_by_email(email: str) -> User | None
    async def get_list(page, filters) -> tuple[list[User], int]
    async def create(data: UserCreate) -> User
    async def update(user: User, data: UserUpdate) -> User
    async def delete(user: User) -> None
    
    # Auth operations
    async def authenticate(email: str, password: str) -> User | None
    async def update_password(user: User, new_password: str) -> User
```

---

## Frontend Structure

### Directory Layout

```
apps/web/
├── src/
│   ├── main.tsx                   # App entry point, providers, routes
│   ├── index.css                  # Global styles + Tailwind
│   │
│   ├── components/
│   │   ├── layout/                # App shell components
│   │   │   ├── app-layout.tsx     # Main layout with sidebar
│   │   │   ├── sidebar.tsx        # Navigation sidebar
│   │   │   ├── header.tsx         # Top header bar
│   │   │   ├── mobile-sidebar.tsx # Mobile navigation
│   │   │   └── toaster.tsx        # Toast notifications
│   │   │
│   │   ├── ui/                    # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   ├── table.tsx
│   │   │   └── ...
│   │   │
│   │   ├── projects/
│   │   │   └── project-modal.tsx  # Create/edit project form
│   │   │
│   │   └── users/
│   │       └── user-modal.tsx     # Create/edit user form
│   │
│   ├── contexts/
│   │   ├── auth-context.tsx       # Authentication state & methods
│   │   └── theme-context.tsx      # Dark/light mode toggle
│   │
│   ├── hooks/
│   │   └── use-toast.ts           # Toast notification hook
│   │
│   ├── lib/
│   │   ├── api.ts                 # API client (fetch wrapper)
│   │   ├── types.ts               # TypeScript type definitions
│   │   └── utils.ts               # Helper functions (cn, formatDate)
│   │
│   └── pages/
│       ├── login.tsx              # Login page
│       ├── dashboard.tsx          # Dashboard with KPIs
│       ├── projects.tsx           # Projects list + CRUD
│       ├── users.tsx              # Users list + CRUD
│       ├── audit-logs.tsx         # Audit log viewer
│       └── settings.tsx           # User settings
│
├── public/                        # Static assets
├── index.html                     # HTML template
├── package.json                   # Dependencies
├── vite.config.ts                 # Vite configuration
├── tailwind.config.js             # Tailwind configuration
├── tsconfig.json                  # TypeScript configuration
├── Dockerfile                     # Container build
└── nginx.conf                     # Nginx configuration
```

### Key Files Explained

#### `src/main.tsx` - App Setup

```tsx
// Provider hierarchy (order matters!)
<QueryClientProvider>     {/* React Query for server state */}
  <ThemeProvider>         {/* Dark/light mode */}
    <AuthProvider>        {/* User authentication state */}
      <BrowserRouter>     {/* Client-side routing */}
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<AppLayout />}>  {/* Protected routes */}
            <Route path="/" element={<DashboardPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/users" element={<UsersPage />} />
            <Route path="/audit-logs" element={<AuditLogsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
      <Toaster />         {/* Toast notifications */}
    </AuthProvider>
  </ThemeProvider>
</QueryClientProvider>
```

#### `src/contexts/auth-context.tsx` - Authentication

```tsx
interface AuthContextType {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}

// On login:
// 1. POST /api/v1/auth/login
// 2. Store tokens in localStorage
// 3. Set user state
// 4. React Query caches user data

// On page load:
// 1. Check localStorage for access_token
// 2. Call GET /api/v1/auth/me to verify
// 3. Set user state or redirect to login
```

#### `src/lib/api.ts` - API Client

```tsx
const api = {
  get: <T>(endpoint, params?) => request<T>(endpoint, { method: 'GET', params }),
  post: <T>(endpoint, data?) => request<T>(endpoint, { method: 'POST', body: data }),
  patch: <T>(endpoint, data?) => request<T>(endpoint, { method: 'PATCH', body: data }),
  delete: <T>(endpoint) => request<T>(endpoint, { method: 'DELETE' }),
}

// Features:
// - Auto-prepends /api/v1 to all endpoints
// - Auto-attaches Authorization: Bearer <token> header
// - Auto-redirects to /login on 401 errors
// - Type-safe with generics
```

#### `src/pages/projects.tsx` - Example Page

```tsx
export function ProjectsPage() {
  // Fetch projects with React Query
  const { data, isLoading } = useQuery({
    queryKey: ['projects', filters],
    queryFn: () => api.get('/projects', filters),
  })

  // Create/update mutation
  const mutation = useMutation({
    mutationFn: (data) => api.post('/projects', data),
    onSuccess: () => {
      queryClient.invalidateQueries(['projects'])
      toast({ title: 'Project created!' })
    },
  })

  return (
    <div>
      <Table data={data?.items} />
      <ProjectModal onSubmit={mutation.mutate} />
      <Pagination total={data?.total} />
    </div>
  )
}
```

---

## Database Models

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                          users                               │
├─────────────────────────────────────────────────────────────┤
│ id              SERIAL PRIMARY KEY                          │
│ email           VARCHAR(255) UNIQUE NOT NULL                │
│ hashed_password VARCHAR(255) NOT NULL                       │
│ full_name       VARCHAR(255) NOT NULL                       │
│ role            ENUM('admin','manager','viewer') NOT NULL   │
│ is_active       BOOLEAN DEFAULT true                        │
│ created_at      TIMESTAMP WITH TIME ZONE                    │
│ updated_at      TIMESTAMP WITH TIME ZONE                    │
│ last_login      TIMESTAMP WITH TIME ZONE                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         projects                             │
├─────────────────────────────────────────────────────────────┤
│ id              SERIAL PRIMARY KEY                          │
│ name            VARCHAR(255) NOT NULL                       │
│ description     TEXT                                        │
│ status          ENUM('draft','active','on_hold',            │
│                      'completed','archived') NOT NULL       │
│ priority        ENUM('low','medium','high','critical')      │
│ budget          INTEGER (in cents)                          │
│ start_date      TIMESTAMP WITH TIME ZONE                    │
│ end_date        TIMESTAMP WITH TIME ZONE                    │
│ owner_id        INTEGER REFERENCES users(id) ON DELETE CASCADE│
│ created_at      TIMESTAMP WITH TIME ZONE                    │
│ updated_at      TIMESTAMP WITH TIME ZONE                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        audit_logs                            │
├─────────────────────────────────────────────────────────────┤
│ id              SERIAL PRIMARY KEY                          │
│ user_id         INTEGER REFERENCES users(id) ON DELETE SET NULL│
│ action          ENUM('login','logout','login_failed',       │
│                      'user_create','user_update',...) NOT NULL│
│ resource_type   VARCHAR(50) NOT NULL                        │
│ resource_id     INTEGER                                     │
│ details         JSONB                                       │
│ ip_address      VARCHAR(45)                                 │
│ user_agent      TEXT                                        │
│ request_id      VARCHAR(36)                                 │
│ created_at      TIMESTAMP WITH TIME ZONE                    │
└─────────────────────────────────────────────────────────────┘
```

### Enums

```python
# User roles
class UserRole(str, Enum):
    admin = "admin"       # Full access
    manager = "manager"   # Create/edit own resources
    viewer = "viewer"     # Read-only access

# Project status
class ProjectStatus(str, Enum):
    draft = "draft"
    active = "active"
    on_hold = "on_hold"
    completed = "completed"
    archived = "archived"

# Project priority
class ProjectPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

# Audit actions
class AuditAction(str, Enum):
    login = "login"
    logout = "logout"
    login_failed = "login_failed"
    user_create = "user_create"
    user_update = "user_update"
    user_delete = "user_delete"
    user_role_change = "user_role_change"
    password_change = "password_change"
    project_create = "project_create"
    project_update = "project_update"
    project_delete = "project_delete"
    project_status_change = "project_status_change"
```

---

## API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/login` | Login and get tokens | No |
| POST | `/refresh` | Refresh access token | No (needs refresh_token) |
| POST | `/logout` | Logout (audit log only) | Yes |
| GET | `/me` | Get current user info | Yes |

### Users (`/api/v1/users`)

| Method | Endpoint | Description | Required Role |
|--------|----------|-------------|---------------|
| GET | `/` | List users (paginated) | Any |
| POST | `/` | Create new user | Admin |
| GET | `/{id}` | Get user by ID | Any |
| PATCH | `/{id}` | Update user | Admin/Manager |
| DELETE | `/{id}` | Delete user | Admin |
| POST | `/me/password` | Change own password | Any |

### Projects (`/api/v1/projects`)

| Method | Endpoint | Description | Required Role |
|--------|----------|-------------|---------------|
| GET | `/` | List projects (paginated) | Any |
| POST | `/` | Create new project | Admin/Manager |
| GET | `/{id}` | Get project by ID | Any |
| PATCH | `/{id}` | Update project | Admin/Manager (own) |
| DELETE | `/{id}` | Delete project | Admin/Manager (own) |

### Audit Logs (`/api/v1/audit-logs`)

| Method | Endpoint | Description | Required Role |
|--------|----------|-------------|---------------|
| GET | `/` | List audit logs (paginated) | Admin |

### Dashboard (`/api/v1/dashboard`)

| Method | Endpoint | Description | Required Role |
|--------|----------|-------------|---------------|
| GET | `/stats` | Get dashboard statistics | Any |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check (no auth) |

---

## Role-Based Access Control (RBAC)

### Permission Matrix

| Action | Admin | Manager | Viewer |
|--------|:-----:|:-------:|:------:|
| **Dashboard** |
| View dashboard stats | ✅ | ✅ | ✅ |
| **Projects** |
| View all projects | ✅ | ✅ | ✅ |
| Create projects | ✅ | ✅ | ❌ |
| Edit any project | ✅ | ❌ | ❌ |
| Edit own projects | ✅ | ✅ | ❌ |
| Delete any project | ✅ | ❌ | ❌ |
| Delete own projects | ✅ | ✅ | ❌ |
| **Users** |
| View all users | ✅ | ✅ | ✅ |
| Create users | ✅ | ❌ | ❌ |
| Edit users | ✅ | ❌ | ❌ |
| Delete users | ✅ | ❌ | ❌ |
| Change user roles | ✅ | ❌ | ❌ |
| **Audit Logs** |
| View audit logs | ✅ | ❌ | ❌ |
| **Settings** |
| Change own password | ✅ | ✅ | ✅ |
| Update profile | ✅ | ✅ | ✅ |

### Implementation

```python
# In app/api/deps.py

def require_role(*allowed_roles: UserRole):
    """Dependency factory for role-based access control."""
    async def role_checker(current_user: User) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return role_checker

# Pre-built dependencies
AdminOnly = Depends(require_role(UserRole.admin))
AdminOrManager = Depends(require_role(UserRole.admin, UserRole.manager))
AnyRole = Depends(require_role(UserRole.admin, UserRole.manager, UserRole.viewer))

# Usage in endpoints
@router.post("")
async def create_user(
    data: UserCreate,
    current_user: User = AdminOnly,  # Only admins can create users
):
    ...
```

---

## Running Locally

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Git

### Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url> admin_panel
cd admin_panel

# 2. Start all services
docker-compose up -d

# 3. Wait for services to be healthy (check logs)
docker-compose logs -f api

# 4. Run database migrations
docker-compose exec api alembic upgrade head

# 5. Seed demo data
docker-compose exec api python seed_db.py

# 6. Open in browser
# http://localhost
```

### Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost | Main application |
| API Docs | http://localhost:8000/api/v1/docs | Swagger UI |
| ReDoc | http://localhost:8000/api/v1/redoc | Alternative docs |
| PostgreSQL | localhost:5432 | Database (user: postgres, pass: postgres) |
| Redis | localhost:6379 | Cache |

### Useful Commands

```bash
# View logs
docker-compose logs -f api          # API logs
docker-compose logs -f web          # Frontend logs
docker-compose logs -f db           # Database logs

# Restart services
docker-compose restart api          # Restart API
docker-compose restart              # Restart all

# Stop everything
docker-compose down                 # Stop containers
docker-compose down -v              # Stop + delete volumes (fresh start)

# Database operations
docker-compose exec api alembic upgrade head     # Run migrations
docker-compose exec api alembic downgrade -1     # Rollback one migration
docker-compose exec api python seed_db.py        # Seed data

# Access database directly
docker-compose exec db psql -U postgres -d admin_panel

# Shell access
docker-compose exec api bash        # API container shell
docker-compose exec web sh          # Frontend container shell
```

---

## Deployment Guide

### Option 1: Render (Backend) + Vercel (Frontend)

This is the recommended approach for beginners. Both have generous free tiers.

#### Step 1: Create PostgreSQL Database (Neon - Free)

1. Go to https://neon.tech and create account
2. Create new project
3. Copy connection string
4. Modify it:
   - Change `postgresql://` to `postgresql+asyncpg://`
   - Add `?sslmode=require` at the end

Example:
```
postgresql+asyncpg://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

#### Step 2: Deploy Backend to Render

1. Go to https://render.com and create account
2. Connect your GitHub repository
3. Click "New" → "Web Service"
4. Configure:

```
Name: admin-panel-api
Root Directory: apps/api
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Add Environment Variables:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Your Neon connection string |
| `SECRET_KEY` | Generate with: `openssl rand -hex 32` |
| `ENVIRONMENT` | `production` |
| `CORS_ORIGINS` | `["https://your-app.vercel.app"]` |

6. Deploy and wait for build to complete

7. Open Render Shell and run:
```bash
alembic upgrade head
python seed_db.py
```

#### Step 3: Deploy Frontend to Vercel

1. Go to https://vercel.com and create account
2. Import your GitHub repository
3. Configure:

```
Framework Preset: Vite
Root Directory: apps/web
Build Command: npm run build
Output Directory: dist
```

4. Add Environment Variable:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://admin-panel-api.onrender.com` |

5. Deploy!

#### Step 4: Update CORS

Go back to Render and update `CORS_ORIGINS` with your actual Vercel URL:
```
["https://your-actual-app.vercel.app"]
```

### Option 2: Railway (All-in-one)

Railway is simpler but has usage-based pricing.

```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add PostgreSQL database
railway add --database postgresql

# Set environment variables in Railway dashboard:
# SECRET_KEY, CORS_ORIGINS, ENVIRONMENT

# Deploy backend
cd apps/api
railway up

# Deploy frontend (separate service)
cd ../web
railway up
```

### Option 3: Self-Hosted (VPS with Docker)

For full control, deploy to a VPS (DigitalOcean, Linode, Hetzner, etc.)

```bash
# On your VPS (Ubuntu 22.04)

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Clone repository
git clone <your-repo> admin_panel
cd admin_panel

# Create production environment file
cat > .env << 'EOF'
ENVIRONMENT=production
SECRET_KEY=your-super-secret-key-here-at-least-32-chars
DATABASE_URL=postgresql+asyncpg://postgres:securepassword@db:5432/admin_panel
POSTGRES_PASSWORD=securepassword
REDIS_URL=redis://redis:6379/0
CORS_ORIGINS=["https://yourdomain.com"]
EOF

# Start services
docker-compose up -d

# Run migrations
docker-compose exec api alembic upgrade head
docker-compose exec api python seed_db.py

# Setup Nginx reverse proxy with SSL (use Certbot)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Environment Variables

### Backend (`apps/api`)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | JWT signing key (32+ chars) | ✅ Yes | - |
| `DATABASE_URL` | PostgreSQL connection string | ✅ Yes | - |
| `REDIS_URL` | Redis connection string | No | `redis://localhost:6379/0` |
| `ENVIRONMENT` | `development` / `production` | No | `development` |
| `DEBUG` | Enable debug logging | No | `false` |
| `CORS_ORIGINS` | Allowed frontend URLs (JSON array) | No | `["http://localhost:5173"]` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT access token lifetime | No | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | JWT refresh token lifetime | No | `7` |

### Frontend (`apps/web`)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `VITE_API_URL` | Backend API URL | No | `/api` (proxied by Nginx) |

---

## Troubleshooting

### Common Issues

#### 1. "Cannot connect to database"

```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Verify connection string
docker-compose exec api python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
```

#### 2. "JWT token invalid" or "401 Unauthorized"

- Check if `SECRET_KEY` is the same across restarts
- Clear browser localStorage and login again
- Verify token hasn't expired (30 min for access token)

#### 3. "CORS error" in browser console

- Verify `CORS_ORIGINS` includes your frontend URL
- Check for trailing slashes (should not have them)
- Format: `["https://example.com"]` (JSON array)

#### 4. "Login fails after seeding"

```bash
# Re-run seed script
docker-compose exec api python seed_db.py

# Check users exist
docker-compose exec db psql -U postgres -d admin_panel -c "SELECT email, role FROM users;"
```

#### 5. Frontend shows blank page

```bash
# Check for build errors
docker-compose logs web

# Rebuild frontend
docker-compose build --no-cache web
docker-compose up -d web
```

#### 6. "Enum value invalid" errors

This is a Python/PostgreSQL enum mismatch. The enum values must be lowercase:
- ✅ `role = UserRole.admin`
- ❌ `role = UserRole.ADMIN`

#### 7. Database migration fails

```bash
# Check current migration status
docker-compose exec api alembic current

# See migration history
docker-compose exec api alembic history

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
docker-compose exec api alembic upgrade head
docker-compose exec api python seed_db.py
```

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review Docker logs: `docker-compose logs -f`
3. Check API documentation: http://localhost:8000/api/v1/docs
4. Verify environment variables are set correctly

---

**Built with ❤️ using FastAPI, React, and modern best practices.**
