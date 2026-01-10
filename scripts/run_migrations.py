#!/usr/bin/env python3
"""
Helper script to run Alembic migrations.

Usage:
    python scripts/run_migrations.py upgrade head
    python scripts/run_migrations.py downgrade -1
"""
import subprocess
import sys
from pathlib import Path

def main():
    api_dir = Path(__file__).parent.parent / "apps" / "api"
    
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_migrations.py <alembic command>")
        print("Example: python scripts/run_migrations.py upgrade head")
        sys.exit(1)
    
    cmd = ["alembic"] + sys.argv[1:]
    print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, cwd=api_dir)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
