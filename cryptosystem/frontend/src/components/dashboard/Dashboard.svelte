<script>
	import { onMount } from "svelte";
    import { userToken } from "../../stores/user";
    import user from "../../stores/user";
	import { AppRail, AppRailAnchor, AppRailTile } from "@skeletonlabs/skeleton";
    import User from "../authentication/User.svelte";
	import PollsInformation from "./PollsInformation.svelte";
	import ManagePolls from "./ManagePolls.svelte";
    import { currentTab } from "../../stores/dashboard";
	import Polls from "./Polls.svelte";
    import isMobileStore from "../../stores/generalStore";

    let isMobile = false;

    isMobileStore.subscribe(value => {
        isMobile = value;
    });

    onMount(() => {
        const urlParams = new URLSearchParams(window.location.search);

        // check user token
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

                 // redirect user to dashboard poll if joined poll by link
                if (urlParams.has("poll_code") || urlParams.has("poll_id")) {
                    $currentTab = 3;
                }
            })
            .catch(error => console.error('Error:', error));           
        }
    })
</script>

<div class="flex h-[100%]">
    {#if !isMobile}
        <AppRail>
            <svelte:fragment slot="lead">
                <AppRailAnchor href="/" >
                    <img class="w-6 h-6 mx-[auto]" src="../house-solid.svg" alt="logo" />
                    <span class="mx-[auto]">Home</span>
                </AppRailAnchor>
            </svelte:fragment>
            
            <AppRailTile bind:group={$currentTab} name="tile-2" value={1} title="tile-2">
                <svelte:fragment slot="lead">
                    <img class="w-6 h-6 mx-[auto]" src="../square-poll-vertical-solid.svg" alt="logo" />
                </svelte:fragment>
                <span>Dashboard</span>
            </AppRailTile>
            <AppRailTile bind:group={$currentTab} name="tile-4" value={3} title="tile-4">
                <svelte:fragment slot="lead">
                    <img class="w-6 h-6 mx-[auto]" src="../check-to-slot-solid.svg" alt="logo" />
                </svelte:fragment>
                <span>Polls</span>
            </AppRailTile>
            <AppRailTile bind:group={$currentTab} name="tile-3" value={2} title="tile-3">
                <svelte:fragment slot="lead">
                    <img class="w-6 h-6 mx-[auto]" src="../table-columns-solid.svg" alt="logo" />
                </svelte:fragment>
                <span>Manage Polls</span>
            </AppRailTile>
            <AppRailTile bind:group={$currentTab} name="tile-1" value={0} title="tile-1">
                <svelte:fragment slot="lead">
                    <img class="w-6 h-6 mx-[auto]" src="../user-solid.svg" alt="logo" />
                </svelte:fragment>
                <span>Personal Information</span>
            </AppRailTile>
        </AppRail>
    {/if}
    <div class="w-[100%]">
        {#if $currentTab == 0}
            <User />
        {:else if $currentTab == 1}
            <PollsInformation />
        {:else if $currentTab == 2}
            <ManagePolls />
        {:else if $currentTab == 3}
            <Polls />
        {/if}
    </div>
</div>

