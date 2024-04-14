from crud import create_poll as create_poll_crud, get_poll_by_id, get_vote_by_poll_and_user_id, get_user_by_id, update_user, update_poll as update_poll_crud, delete_poll as delete_poll_crud, get_polls as get_polls_crud, get_votes_by_poll_id, delete_votes_by_poll_id
from models import Poll, Candidate, Vote, PollResults, User
from paillier import add, generate_keys, encrypt, decrypt
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime

async def create_poll(poll_data: Poll, user_id: str):
    poll_obj = Poll(**poll_data.model_dump())
    
    # create encryption/decryption keys
    public_key, private_key = await generate_keys()

    # encrypt candidate votes count (initially 0)
    if not poll_obj.candidates is None:
        for candidate in poll_obj.candidates:
            candidate.tally = str(await encrypt(public_key, 0))

    # set encryption key
    poll_obj.encryption_key = str(public_key)

    poll_obj.created_at = datetime.now()
    poll_obj.updated_at = datetime.now()
    poll_obj.created_by = user_id

    # create the poll
    poll_id = await create_poll_crud(poll_obj)
    poll = await get_poll_by_id(poll_id)

    # set private key for user
    user = await get_user_by_id(user_id)
    if user.polls is None:
        user.polls = {}
    user.polls[str(poll.id)] = str(private_key)

    # update user with private key
    await update_user(str(user_id), user)

async def update_poll(poll_id: str, poll_data: Poll):
    poll = await get_poll_by_id(poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    poll.title = poll_data.title
    poll.description = poll_data.description
    poll.is_private = poll_data.is_private
    poll.multiple_choice = poll_data.multiple_choice
    
    poll.updated_at = datetime.now()

    return await update_poll_crud(poll_id, poll)

async def add_vote(poll_id: str, vote: Vote, user_id: str):
    poll = await get_poll_by_id(poll_id)
    public_key = eval(poll.encryption_key)

    # add vote
    if poll.candidates is not None:
        public_key = eval(poll.encryption_key)
        for voteCandidate, pollCandidate in zip(vote.candidates, poll.candidates):
            pollCandidate.tally = str(await add(public_key, int(pollCandidate.tally), int(voteCandidate.tally)))

    await update_poll_crud(poll_id, poll)

async def delete_poll(poll_id: str):
    poll = await get_poll_by_id(poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    # remove poll from creator user
    user = await get_user_by_id(str(poll.created_by))
    user.polls.pop(str(ObjectId(poll_id)))
    await update_user(str(poll.created_by), user)

    # remove votes
    await delete_votes_by_poll_id(poll_id)

    # delete poll
    return await delete_poll_crud(poll_id)

async def get_polls(user_id: str):
    polls = await get_polls_crud()
    newPolls = []

    for poll in polls:
        # only add votes that the user has not voted on
        userVote = await get_vote_by_poll_and_user_id(poll.id, user_id)
        if userVote is None:
            newPolls.append(poll)

    return newPolls

async def get_results(poll_id: str, user: User):
    poll = await get_poll_by_id(poll_id)
    print(user)
    pollResults = PollResults(
        poll_id=poll_id,
        total_votes=0,
        candidates=poll.candidates,
        county_statistics={},
        votes_this_week={
            'monday': 0,
            'tuesday': 0,
            'wednesday': 0,
            'thursday': 0,
            'friday': 0,
            'saturday': 0,
            'sunday': 0
        }
    )

    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")

    if poll_id in user.polls or poll.is_revealed:
        votes = await get_votes_by_poll_id(poll_id)
        pollResults.total_votes = len(votes)
        pollResults.votes_this_week = add_votes_by_days(pollResults.votes_this_week, votes)

        # go through each vote, read user and add to county statistics
        for vote in votes:
            currentUser = await get_user_by_id(vote.user_id)
            if currentUser.county in pollResults.county_statistics:
                pollResults.county_statistics[currentUser.county] += 1
            else:
                pollResults.county_statistics[currentUser.county] = 1

        # decrypt candidates tallies
        for candidate in pollResults.candidates:
            candidate.tally = await decrypt(eval(poll.encryption_key), eval(user.polls[poll_id]), eval(candidate.tally))
    else:
        raise HTTPException(status_code=403, detail="Poll results are not revealed")
    
    return pollResults

async def get_general_results(user_polls: dict):
    polls = await get_polls_crud()
    pollResults = PollResults(
        total_votes=0,
        candidates=[],
        county_statistics={},
        votes_this_week={
            'monday': 0,
            'tuesday': 0,
            'wednesday': 0,
            'thursday': 0,
            'friday': 0,
            'saturday': 0,
            'sunday': 0
        }
    )

    for poll in polls:
        if str(poll.id) in user_polls or poll.is_revealed:
            votes = await get_votes_by_poll_id(poll.id)
            pollResults.total_votes += len(votes)
            pollResults.votes_this_week = add_votes_by_days(pollResults.votes_this_week, votes)
            # go through each vote, read user and add to county statistics
            for vote in votes:
                user = await get_user_by_id(vote.user_id)
                if user.county in pollResults.county_statistics:
                    pollResults.county_statistics[user.county] += 1
                else:
                    pollResults.county_statistics[user.county] = 1
    
    return pollResults

def add_votes_by_days(votes_this_week ,votes: list[Vote]):
    for vote in votes:
        created_at = vote.created_at
        day = created_at.strftime('%A').lower()
        votes_this_week[day] += 1
    return votes_this_week