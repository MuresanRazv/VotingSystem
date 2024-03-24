<script>
	import { goto } from '$app/navigation';
    import { AppBar } from '@skeletonlabs/skeleton';
</script>

<AppBar>
	<svelte:fragment slot="lead"><img style="filter: invert(100%); width: 35px; heigth: 35px;" src="./privacy-document-icon.svg" alt="img"/></svelte:fragment>
	CyberPolls
	<svelte:fragment slot="trail">
        <button type="button" class="btn bg-initial" on:click={() => goto('/')}>Home</button>
        <button type="button" class="btn bg-initial" on:click={() => goto('/register')}>Register</button>
        <button type="button" class="btn bg-initial" on:click={() => goto('/login')}>Login</button>
        <button type="button" class="btn bg-initial" on:click={() => goto('/dashboard')}>Dashboard</button>
    </svelte:fragment>
</AppBar>
