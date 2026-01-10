# Admin Panel

A production-ready admin panel with FastAPI backend and React frontend. Built for speed, security, and developer experience.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND                                   │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  React + Vite + TailwindCSS + shadcn/ui                     │    │
│  │  • React Query for caching & optimistic updates             │    │
│  │  • React Router for navigation                              │    │
│  │  • JWT tokens stored in localStorage                        │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ HTTP/REST
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            BACKEND                                   │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  FastAPI                                                     │    │
│  │  • JWT Authentication (access + refresh tokens)             │    │
│  │  • RBAC (admin, manager, viewer)                            │    │
│  │  • Request ID tracking & structured logging                 │    │
│  │  • Audit logging for sensitive actions                      │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                        │                    │                        │
│                        ▼                    ▼                        │
│  ┌──────────────────────────┐  ┌──────────────────────────┐        │
│  │  PostgreSQL              │  │  Redis                    │        │
│  │  • Users, Projects       │  │  • Session cache          │        │
│  │  • Audit logs            │  │  • Background jobs        │        │
│  │  • Alembic migrations    │  │                           │        │
│  └──────────────────────────┘  └──────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
```

## Features

### Backend
- **FastAPI** with async SQLAlchemy
- **JWT Authentication** with access and refresh tokens
- **RBAC** with three roles: admin, manager, viewer
- **CRUD APIs** for Projects and Users
- **Pagination, filtering, sorting** on all list endpoints
- **Audit logging** for all sensitive actions
- **Structured logging** with request ID tracking
- **Alembic** database migrations
- **Docker** ready

### Frontend
- **React + Vite** for fast development and builds
- **TailwindCSS + shadcn/ui** for beautiful, accessible components
- **React Query** for server state management with caching
- **React Router** for client-side routing
- **Dark mode** support
- **Responsive** design (mobile + desktop)
- **Optimistic updates** for better UX

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repo-url> admin_panel
cd admin_panel

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec api alembic upgrade head

# Seed demo data
docker-compose exec api python -c "
import asyncio
import sys
sys.path.insert(0, '/app')
from scripts.seed import seed_database
asyncio.run(seed_database())
"

# Open http://localhost in your browser
```

### Local Development

#### Backend

```bash
cd apps/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables (or create .env file)
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/admin_panel"
export SECRET_KEY="your-secret-key"

# Run migrations
alembic upgrade head

# Seed demo data
cd ../..
python scripts/seed.py
cd apps/api

# Start the server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd apps/web

# Install dependencies
npm install

# Start dev server
npm run dev
```

Open http://localhost:5173 in your browser.

## Demo Credentials

| Role    | Email               | Password    |
|---------|---------------------|-------------|
| Admin   | admin@example.com   | admin123    |
| Manager | manager@example.com | manager123  |
| Viewer  | viewer@example.com  | viewer123   |

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### Example Requests

#### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
```

#### List Projects (with auth)
```bash
curl http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer <access_token>"
```

#### Create Project
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Project", "status": "active", "priority": "high"}'
```

## RBAC (Role-Based Access Control)

| Action              | Admin | Manager | Viewer |
|---------------------|-------|---------|--------|
| View dashboard      | ✅    | ✅      | ✅     |
| View projects       | ✅    | ✅      | ✅     |
| Create projects     | ✅    | ✅      | ❌     |
| Edit any project    | ✅    | ❌      | ❌     |
| Edit own projects   | ✅    | ✅      | ❌     |
| Delete projects     | ✅    | Own     | ❌     |
| View users          | ✅    | ✅      | ✅     |
| Create users        | ✅    | ❌      | ❌     |
| Edit users          | ✅    | ❌      | ❌     |
| Delete users        | ✅    | ❌      | ❌     |
| Change user roles   | ✅    | ❌      | ❌     |
| View audit logs     | ✅    | ❌      | ❌     |

## Project Structure

```
admin_panel/
├── apps/
│   ├── api/                    # FastAPI backend
│   │   ├── app/
│   │   │   ├── api/            # API routes
│   │   │   │   ├── deps.py     # Dependencies (auth, etc.)
│   │   │   │   └── v1/
│   │   │   │       ├── endpoints/
│   │   │   │       └── router.py
│   │   │   ├── core/           # Core functionality
│   │   │   │   ├── config.py   # Settings
│   │   │   │   ├── database.py # DB setup
│   │   │   │   ├── security.py # JWT, hashing
│   │   │   │   ├── logging.py  # Structured logs
│   │   │   │   └── middleware.py
│   │   │   ├── models/         # SQLAlchemy models
│   │   │   ├── schemas/        # Pydantic schemas
│   │   │   ├── services/       # Business logic
│   │   │   └── main.py         # App entry point
│   │   ├── alembic/            # DB migrations
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   └── web/                    # React frontend
│       ├── src/
│       │   ├── components/     # UI components
│       │   │   ├── layout/     # App layout
│       │   │   ├── ui/         # shadcn components
│       │   │   ├── projects/   # Project components
│       │   │   └── users/      # User components
│       │   ├── contexts/       # React contexts
│       │   ├── hooks/          # Custom hooks
│       │   ├── lib/            # Utilities
│       │   ├── pages/          # Page components
│       │   └── main.tsx        # App entry point
│       ├── package.json
│       └── Dockerfile
│
├── scripts/
│   ├── seed.py                 # Database seeder
│   └── run_migrations.py       # Migration helper
│
├── docker-compose.yml          # Docker config
└── README.md
```

## Deployment

### Backend (Render/Railway/Fly.io)

#### Render

1. Create a new Web Service
2. Connect your GitHub repository
3. Set root directory: `apps/api`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `DATABASE_URL` - Your PostgreSQL connection string
   - `SECRET_KEY` - Random secure string (32+ chars)
   - `ENVIRONMENT` - `production`
   - `CORS_ORIGINS` - `["https://your-frontend.vercel.app"]`

#### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link project
railway login
railway link

# Deploy
cd apps/api
railway up
```

#### Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
cd apps/api
fly launch
fly deploy
```

### Frontend (Vercel)

1. Import project from GitHub
2. Set root directory: `apps/web`
3. Framework preset: Vite
4. Add environment variable:
   - `VITE_API_URL` - Your backend URL (e.g., `https://api.example.com`)

Or using CLI:

```bash
cd apps/web
npx vercel --prod
```

### Database (PostgreSQL)

Recommended managed options:
- **Neon** (free tier available)
- **Supabase** (free tier available)
- **Railway PostgreSQL**
- **Render PostgreSQL**

## Environment Variables

### Backend

| Variable          | Description                    | Default                     |
|-------------------|--------------------------------|-----------------------------|
| `DATABASE_URL`    | PostgreSQL connection string   | `postgresql+asyncpg://...`  |
| `SECRET_KEY`      | JWT signing key                | -                           |
| `ENVIRONMENT`     | development/staging/production | `development`               |
| `DEBUG`           | Enable debug mode              | `false`                     |
| `REDIS_URL`       | Redis connection string        | `redis://localhost:6379/0`  |
| `CORS_ORIGINS`    | Allowed CORS origins           | `["http://localhost:5173"]` |

### Frontend

| Variable       | Description     | Default |
|----------------|-----------------|---------|
| `VITE_API_URL` | Backend API URL | `/api`  |

## Future Extensions

- [ ] Two-factor authentication (2FA)
- [ ] OAuth providers (Google, GitHub)
- [ ] File uploads with S3
- [ ] Real-time notifications with WebSockets
- [ ] Email notifications
- [ ] API rate limiting
- [ ] Terraform/Pulumi infrastructure as code
- [ ] CI/CD with GitHub Actions
- [ ] End-to-end tests with Playwright
- [ ] OpenTelemetry tracing

## License

MIT
