<script>
	import { goto } from "$app/navigation";
	import { login } from "../../helper/authentication";
	import { userToken } from "../../stores/user";
    import isMobileStore from "../../stores/generalStore";
    let email = ""
    let password = ""
    let isMobile = false;

    isMobileStore.subscribe(value => {
        isMobile = value;
    });

    function handleLogin() {
        login(email, password)
        .then(data => {
            console.log('ha')
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

<div class="{!isMobile ? 'w-[50vw]': ''} mx-[auto] my-[auto]">
	<header class="text-center pt-5">
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

    <footer class="flex justify-center">
        <button type="button" class="btn variant-filled-secondary" on:click={handleLogin}>
            Login
        </button>
    </footer>
</div>  