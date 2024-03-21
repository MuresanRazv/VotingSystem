# app/crud/__init__.py

from .user import create_user, get_user_by_email, get_user_by_id, update_user, delete_user
from .candidate import create_candidate, get_candidate, update_candidate, delete_candidate