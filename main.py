"""
Entry point for the application.
Run with: uvicorn main:app --reload
"""
from app.main import app

__all__ = ["app"]

