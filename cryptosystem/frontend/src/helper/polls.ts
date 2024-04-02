export type Candidate = {
  _id?: string,
  name: string,
  description: string,
}

export type Poll = {
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

async function updatePoll(pollId: string, pollData: Poll) {
  return await fetch(`http://127.0.0.1:8000/api/polls/${pollId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify(pollData)
  })
  .then(response => response.json())
}

async function addCandidate(pollId: string, candidate: Candidate) {
  return await fetch(`http://127.0.0.1:8000/api/polls/${pollId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify(candidate)
  })
  .then(response => response.json())
}

async function removeCandidate(pollId: string, candidateId: string) {
  return await fetch(`http://127.0.0.1:8000/api/polls/${pollId}/candidates/${candidateId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(response => response.json())
}

export { getUserPolls, updatePoll };

