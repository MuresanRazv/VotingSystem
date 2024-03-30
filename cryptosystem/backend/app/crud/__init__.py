# app/crud/__init__.py

from .user import create_user, get_user_by_email, get_user_by_id, update_user, delete_user, get_current_active_user
from .candidate import create_candidate, get_candidate, update_candidate, delete_candidate
from .poll import create_poll, get_polls_by_user_id, get_poll_by_id, get_polls, delete_poll, update_poll, create_poll_candidate, remove_poll_candidate, update_poll_candidate
from .vote import create_vote, get_votes_by_poll_id, get_votes_by_user_id, get_vote_by_id, delete_vote, delete_votes_by_poll_id, delete_votes_by_user_id, update_vote