import { PUBLIC_BASE_API_URL } from "$env/static/public";

async function register(user: any, password: string) {
    return fetch(PUBLIC_BASE_API_URL + `/users`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: `${user.username}`,
            email: `${user.email}`,
            password: `${password}`,
            firstname: `${user.firstname}`,
            lastname: `${user.lastname}`,
            county: `${user.county}`,
            city: `${user.city}`
        })
    })
    .then(response => {
        return response.json();
    })
}

async function updateInformation(user: any) {
    return fetch(PUBLIC_BASE_API_URL + `/users/${user._id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
            firstname: `${user.firstname}`,
            lastname: `${user.lastname}`,
            county: `${user.county}`,
            city: `${user.city}`
        })
    })
}

async function login(email: string, password: string) {
    return fetch(PUBLIC_BASE_API_URL + '/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json()
)}
    
export { register, updateInformation, login };