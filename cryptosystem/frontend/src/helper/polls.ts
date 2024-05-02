import type { Poll } from "../stores/polls"
import { PUBLIC_BASE_API_URL } from "$env/static/public";

async function getUserPolls() {
  return await fetch(PUBLIC_BASE_API_URL + `/polls/me`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }
    return response.json();
  })
  .catch(error => {
    window.location.href = '/login';
  });
}

async function getPublicPolls() {
  return await fetch(PUBLIC_BASE_API_URL + `/polls`, {
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
  
  return await fetch(PUBLIC_BASE_API_URL + `/polls/${poll._id}`, {
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
  
  return await fetch(PUBLIC_BASE_API_URL + `/polls`, {
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
      multiple_choice: poll.multiple_choice,
      start_date: poll.start_date,
      end_date: poll.end_date
    })
  })  
}

async function removePoll(poll_id: string) {
  return await fetch(PUBLIC_BASE_API_URL + `/polls/${poll_id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
}

async function getResults(poll_id: string) {
  return await fetch(PUBLIC_BASE_API_URL + `/polls/${poll_id}/results`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(response => response.json());
}

async function getGeneralResults() {
  return await fetch(PUBLIC_BASE_API_URL + `/polls/results`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }
    return response.json();
  })
  .catch(error => {
    window.location.href = '/login';
  });
}

async function publishPoll(poll_id: string) {
  return await fetch(PUBLIC_BASE_API_URL + `/polls/${poll_id}/publish`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
}

async function getPrivatePoll(poll_code: string) {
  return await fetch(PUBLIC_BASE_API_URL + `/polls/private/${poll_code}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(response => response.json());
}

async function getPublicPoll(poll_id: string) {
  return await fetch(PUBLIC_BASE_API_URL + `/polls/${poll_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(response => response.json());
}

export { getUserPolls, updatePoll, createPoll, removePoll, getPublicPolls, getResults, getGeneralResults, publishPoll, getPrivatePoll, getPublicPoll };

