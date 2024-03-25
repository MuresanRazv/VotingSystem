<script>
	import { onMount } from "svelte";
    import { userToken } from "../stores/user";
    import user from "../stores/user";
	import { AppRail, AppRailAnchor, AppRailTile } from "@skeletonlabs/skeleton";
    import User from "./User.svelte";
	import Polls from "./Polls.svelte";

    onMount(() => {
        if (!$userToken) {
            window.location.href = '/login'
        } else {
            fetch('http://127.0.0.1:8000/api/users/me', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            })
            .then(response => {
                if (response.status === 401) {
                    localStorage.removeItem('access_token')
                    window.location.href = '/login'
                } else {
                    return response.json()
                }
            })
            .then(data => {
                user.set(data)
            })
            .catch(error => console.error('Error:', error))
        }
    })

    let currentTile = 0
</script>

<style>
    .dashboard {
        display: flex;
        flex-direction: row;
        height: 100%;
    }

    .content {
        width: 100%;
    }
</style>

<div class="dashboard">
    <AppRail>
        <svelte:fragment slot="lead">
            <AppRailAnchor href="/" >(icon)</AppRailAnchor>
        </svelte:fragment>
        
        <AppRailTile bind:group={currentTile} name="tile-1" value={0} title="tile-1">
            <svelte:fragment slot="lead">(icon)</svelte:fragment>
            <span>Tile 1</span>
        </AppRailTile>
        <AppRailTile bind:group={currentTile} name="tile-2" value={1} title="tile-2">
            <svelte:fragment slot="lead">(icon)</svelte:fragment>
            <span>Tile 2</span>
        </AppRailTile>
        <AppRailTile bind:group={currentTile} name="tile-3" value={2} title="tile-3">
            <svelte:fragment slot="lead">(icon)</svelte:fragment>
            <span>Tile 3</span>
        </AppRailTile>
    
        <svelte:fragment slot="trail">
            <AppRailAnchor href="/" target="_blank" title="Account">(icon)</AppRailAnchor>
        </svelte:fragment>
    </AppRail>
    <div class="content">
        {#if currentTile == 0}
            <User />
        {:else if currentTile == 1}
            <Polls />
        {/if}
    </div>
</div>

