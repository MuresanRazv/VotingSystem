export type Candidate = {
  name: string,
  description: string,
}

export type Poll = {
  _id?: string,
  title: string,
  description: string,
  candidates: Candidate[],
  created_at: string,
  updated_at: string,
  is_private: boolean,
  multiple_choice: boolean,
}

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

export { getUserPolls, updatePoll };

