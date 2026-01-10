#!/usr/bin/env python3
"""
Seed script to populate the database with demo data.

Usage:
    python scripts/seed.py

Make sure to run this from the project root with the API virtualenv activated.
"""
import asyncio
import sys
from pathlib import Path

# Add the api directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "api"))

from datetime import datetime, timedelta, timezone
import random

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.core.database import Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus, ProjectPriority
from app.models.audit_log import AuditLog, AuditAction


async def seed_database():
    """Seed the database with demo data."""
    print("🌱 Starting database seeding...")
    
    # Create engine and session
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        # Check if data already exists
        from sqlalchemy import select, func
        result = await session.execute(select(func.count(User.id)))
        if result.scalar_one() > 0:
            print("⚠️  Database already has data. Skipping seed.")
            return
        
        # Create demo users
        print("👤 Creating demo users...")
        users = [
            User(
                email="admin@example.com",
                full_name="Admin User",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                is_active=True,
            ),
            User(
                email="manager@example.com",
                full_name="Manager User",
                hashed_password=get_password_hash("manager123"),
                role=UserRole.MANAGER,
                is_active=True,
            ),
            User(
                email="viewer@example.com",
                full_name="Viewer User",
                hashed_password=get_password_hash("viewer123"),
                role=UserRole.VIEWER,
                is_active=True,
            ),
            User(
                email="john.doe@example.com",
                full_name="John Doe",
                hashed_password=get_password_hash("password123"),
                role=UserRole.MANAGER,
                is_active=True,
            ),
            User(
                email="jane.smith@example.com",
                full_name="Jane Smith",
                hashed_password=get_password_hash("password123"),
                role=UserRole.VIEWER,
                is_active=True,
            ),
        ]
        
        for user in users:
            session.add(user)
        await session.flush()
        
        print(f"   ✅ Created {len(users)} users")
        
        # Create demo projects
        print("📁 Creating demo projects...")
        project_names = [
            ("Website Redesign", "Complete overhaul of the company website with modern design"),
            ("Mobile App Development", "Native iOS and Android app for customers"),
            ("API Integration", "Third-party API integrations for payment and shipping"),
            ("Data Analytics Platform", "Internal analytics dashboard for business metrics"),
            ("Security Audit", "Comprehensive security review and penetration testing"),
            ("Cloud Migration", "Migrate on-premise infrastructure to AWS"),
            ("Customer Portal", "Self-service portal for customer account management"),
            ("Inventory System", "Real-time inventory tracking and management"),
        ]
        
        statuses = list(ProjectStatus)
        priorities = list(ProjectPriority)
        
        projects = []
        for i, (name, description) in enumerate(project_names):
            project = Project(
                name=name,
                description=description,
                status=statuses[i % len(statuses)],
                priority=priorities[i % len(priorities)],
                budget=random.randint(10000, 500000) * 100,  # In cents
                owner_id=users[i % 3].id,  # Distribute among first 3 users
                start_date=datetime.now(timezone.utc) - timedelta(days=random.randint(0, 60)),
            )
            projects.append(project)
            session.add(project)
        
        await session.flush()
        print(f"   ✅ Created {len(projects)} projects")
        
        # Create demo audit logs
        print("📋 Creating demo audit logs...")
        actions = [
            (AuditAction.LOGIN, "auth", None),
            (AuditAction.USER_CREATE, "user", 2),
            (AuditAction.PROJECT_CREATE, "project", 1),
            (AuditAction.PROJECT_UPDATE, "project", 1),
            (AuditAction.USER_ROLE_CHANGE, "user", 3),
            (AuditAction.PROJECT_STATUS_CHANGE, "project", 2),
            (AuditAction.LOGIN, "auth", None),
            (AuditAction.PROJECT_CREATE, "project", 3),
        ]
        
        for i, (action, resource_type, resource_id) in enumerate(actions):
            log = AuditLog(
                user_id=users[i % len(users)].id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details={"demo": True},
                ip_address="127.0.0.1",
                created_at=datetime.now(timezone.utc) - timedelta(hours=i * 2),
            )
            session.add(log)
        
        await session.flush()
        print(f"   ✅ Created {len(actions)} audit logs")
        
        await session.commit()
    
    await engine.dispose()
    
    print("\n✨ Database seeding complete!")
    print("\n📝 Demo Credentials:")
    print("   Admin:   admin@example.com / admin123")
    print("   Manager: manager@example.com / manager123")
    print("   Viewer:  viewer@example.com / viewer123")


if __name__ == "__main__":
    asyncio.run(seed_database())
