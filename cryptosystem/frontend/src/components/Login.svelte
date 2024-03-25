<style>
    .card {
        width: 50vw;
        margin: 40px auto;
    }

    .card-header {
        text-align: center;
    }

    .card-footer {
        display: flex;
        justify-content: center;
    }
</style>

<script>
	import { goto } from "$app/navigation";
	import { userToken } from "../stores/user";
    let email = ""
    let password = ""

    function handleLogin() {
        fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        })
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('access_token', data.access_token)
            $userToken
            window.location.href = '/dashboard'
        })
        .catch(error => console.error('Error:', error))
    }
</script>

{#if $userToken}
    {goto('/dashboard')}
{/if}

<div class="card">
	<header class="card-header">
        <h2 class="h2">
            Login
        </h2>
    </header>

    <section class="p-4">
        <label class="label">
            <span>Email</span>
            <input class="input" type="email" placeholder="Email" bind:value={email} />
        </label>
        <label class="label">
            <span>Password</span>
            <input class="input" type="password" placeholder="Password" bind:value={password} />
        </label>    
    </section>

    <footer class="card-footer">
        <button type="button" class="btn variant-filled-secondary" on:click={handleLogin}>
            Login
        </button>
    </footer>
</div>  