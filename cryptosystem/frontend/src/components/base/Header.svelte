<script>
	import { goto } from '$app/navigation';
    import { AppBar } from '@skeletonlabs/skeleton';
    import { userToken } from '../../stores/user';
	import { browser } from '$app/environment';
</script>

<AppBar>
	<svelte:fragment slot="lead"><img style="width: 35px; heigth: 35px;" src="./privacy-document-icon.svg" alt="img"/></svelte:fragment>
	CyberPolls
	<svelte:fragment slot="trail">
        <button type="button" class="btn bg-initial" on:click={() => goto('/')}>Home</button>
        <button type="button" class="btn bg-initial" on:click={() => goto('/dashboard')}>Dashboard</button>
        {#if !$userToken}
            <button type="button" class="btn bg-initial" on:click={() => goto('/register')}>Register</button>
            <button type="button" class="btn bg-initial" on:click={() => goto('/login')}>Login</button>
        {:else}
            <button type="button" class="btn bg-initial" on:click={() => {
                localStorage.removeItem('access_token');
                window.location.href = '/';
            }}>Logout</button>
        {/if}
    </svelte:fragment>
</AppBar>
