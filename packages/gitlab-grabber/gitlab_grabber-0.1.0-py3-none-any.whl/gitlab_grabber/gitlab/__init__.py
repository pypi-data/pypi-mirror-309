"""Gitlab package."""

__all__ = ["get_project", "clone_all_repositories"]

from .project_handler import get_project
from .clone_repository import clone_all_repositories
