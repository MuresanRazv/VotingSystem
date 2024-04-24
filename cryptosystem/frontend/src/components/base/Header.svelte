<script lang="ts">
	import { goto } from '$app/navigation';
    import { AppBar, initializeStores } from '@skeletonlabs/skeleton';
    import { userToken } from '../../stores/user';
	import { browser } from '$app/environment';
    import { getDrawerStore } from "@skeletonlabs/skeleton";
    import type { DrawerSettings } from '@skeletonlabs/skeleton';
    import { Drawer } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';

    let isMobile = false;

    onMount(() => {
        window.addEventListener('resize', () => {
            isMobile = window.innerWidth < 768;
        });
    });

    initializeStores();
    const drawerStore = getDrawerStore();
    const drawerSettings: DrawerSettings = {
        position: 'right',
        width: 'w-[50%]'
    };

    function handleDrawer() {
        drawerStore.open(drawerSettings);
    }
</script>

<Drawer />

<AppBar>
	<svelte:fragment slot="lead"><img style="width: 35px; heigth: 35px;" src="./privacy-document-icon.svg" alt="img"/></svelte:fragment>
	CyberPolls
	<svelte:fragment slot="trail">
        {#if !isMobile}
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
        {:else}
            <button on:click={handleDrawer}>
                <img src="../bars-solid.svg" alt="menu" class="w-6 h-6" />
            </button>
        {/if}
    </svelte:fragment>
</AppBar>
