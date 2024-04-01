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

export { getUserPolls };