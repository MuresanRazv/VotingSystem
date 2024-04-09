# app/crud/__init__.py

from .user import create_user, get_user_by_email, get_user_by_id, update_user, delete_user, get_current_active_user
from .poll import create_poll, get_polls_by_user_id, get_poll_by_id, get_polls, delete_poll, update_poll
from .vote import create_vote, get_votes_by_poll_id, get_votes_by_user_id, get_vote_by_id, delete_vote, delete_votes_by_poll_id, delete_votes_by_user_id, update_vote, get_vote_by_poll_and_user_id, get_weekly_votes, get_monthly_votes, get_weekly_votes_by_poll_id