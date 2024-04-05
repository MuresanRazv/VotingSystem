import type { Poll, Candidate } from "../stores/polls"


async function getUserPolls() {
  return await fetch(`http://127.0.0.1:8000/api/polls/me`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(response => response.json())
}

async function updatePoll(poll: Poll) {
  if (!poll.candidates) {
    poll.candidates = []
  }
  // remove id's from candidates, they're not needed
  poll.candidates = poll.candidates.map(candidate => {
    return {
      name: candidate.name,
      description: candidate.description
    }
  })
  
  return await fetch(`http://127.0.0.1:8000/api/polls/${poll._id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify({
      title: poll.title,
      description: poll.description,
      candidates: poll.candidates,
      is_private: poll.is_private,
      multiple_choice: poll.multiple_choice
    })
  })
}

async function createPoll(poll: Poll) {
  if (!poll.candidates) {
    poll.candidates = []
  }
  // remove id's from candidates, they're not needed
  if (poll.candidates) {
    poll.candidates = poll.candidates.map(candidate => {
      return {
        name: candidate.name,
        description: candidate.description
      }
    })
  }
  
  return await fetch(`http://127.0.0.1:8000/api/polls`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify({
      title: poll.title,
      description: poll.description,
      candidates: poll.candidates,
      is_private: poll.is_private,
      multiple_choice: poll.multiple_choice
    })
  })  
}

async function removePoll(poll_id: string) {
  return await fetch(`http://127.0.0.1:8000/api/polls/${poll_id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
}

export { getUserPolls, updatePoll, createPoll, removePoll };

