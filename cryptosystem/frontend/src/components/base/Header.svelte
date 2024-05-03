<script lang="ts">
    import { goto } from '$app/navigation';
    import { AppBar, initializeStores } from '@skeletonlabs/skeleton';
    import { userToken } from '../../stores/user';
    import { browser } from '$app/environment';
    import { getDrawerStore } from "@skeletonlabs/skeleton";
    import type { DrawerSettings } from '@skeletonlabs/skeleton';
    import { Drawer } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
    import { currentTab } from '../../stores/dashboard';
    import isMobileStore from '../../stores/generalStore';

    let isMobile = false;
    isMobileStore.subscribe(value => {
        isMobile = value;
    });

    initializeStores();
    const drawerStore = getDrawerStore();
    const drawerSettings: DrawerSettings = {
        position: 'right',
        width: 'w-[80%]',
    };

    function handleDrawer() {
        drawerStore.open(drawerSettings);
    }
</script>

<Drawer>
    <div class="flex flex-col gap-5 p-5">
        <button type="button" class="btn bg-secondary-800" on:click={() => { goto('/'); drawerStore.close(); }}>
            <img class="w-5 h-5" src="../house-solid.svg" alt="logo" />
            <span class="mx-[auto]">Home</span>
        </button>
        {#if !$userToken}
                <button type="button" class="btn bg-secondary-800" on:click={() => { goto('/register'); drawerStore.close() }}>Register</button>
                <button type="button" class="btn bg-secondary-800" on:click={() => { goto('/login'); drawerStore.close() }}>Login</button>
        {:else}
            <button type="button" class="btn bg-secondary-800" on:click={() => { goto('/dashboard'); drawerStore.close(); $currentTab = 1; }}>
                <img class="w-5 h-5" src="../square-poll-vertical-solid.svg" alt="logo" />
                <span class="mx-[auto]">Dashboard</span>
            </button>
            <button type="button" class="btn bg-secondary-800" on:click={() => { goto('/dashboard'); drawerStore.close(); $currentTab = 3; }}>
                <img class="w-5 h-5" src="../check-to-slot-solid.svg" alt="logo" />
                <span class="mx-[auto]">Polls</span>
            </button>
            <button type="button" class="btn bg-secondary-800" on:click={() => { goto('/dashboard'); drawerStore.close(); $currentTab = 2; }}>
                <img class="w-5 h-5" src="../table-columns-solid.svg" alt="logo" />
                <span class="mx-[auto]">Manage Polls</span>
            </button>
            <button type="button" class="btn bg-secondary-800" on:click={() => { goto('/dashboard'); drawerStore.close(); $currentTab = 0; }}>
                <img class="w-5 h-5" src="../../user-solid.svg" alt="logo" />
                <span class="mx-[auto]">Personal Information</span>
            </button>
            <button type="button" class="btn bg-error-600" on:click={() => {
                localStorage.removeItem('access_token');
                window.location.href = '/';
		drawerStore.close();
            }}>Logout</button>
        {/if}
    </div>
</Drawer>

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
