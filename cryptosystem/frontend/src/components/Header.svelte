<script>
    import { AppBar } from '@skeletonlabs/skeleton';
</script>

<AppBar>
	<svelte:fragment slot="lead">(icon)</svelte:fragment>
	CyberPolls
	<svelte:fragment slot="trail">
        <button type="button" class="btn bg-initial">Home</button>
        <button type="button" class="btn bg-initial">Register</button>
        <button type="button" class="btn bg-initial">Login</button>
        <button type="button" class="btn bg-initial">Dashboard</button>
    </svelte:fragment>
</AppBar>
