<script lang="ts">
    import user from "../../stores/user";
    import romaniaCities from "../../stores/locations"; 
    import { Toast, getToastStore } from '@skeletonlabs/skeleton';
    import type { ToastSettings, ToastStore } from '@skeletonlabs/skeleton';
    import { initializeStores } from '@skeletonlabs/skeleton';
	import { updateInformation } from "../../helper/authentication";
    import isMobileStore from "../../stores/generalStore";

    let isMobile = false;

    isMobileStore.subscribe(value => {
        isMobile = value;
    });

    initializeStores();
    const toastStore = getToastStore();
    const t: ToastSettings = {
	    message: 'Please fill all the fields',
    };

    function handleUpdateInformation() {
        if ($user.firstname == '' || $user.lastname == '' || $user.county == '' || $user.county == '') {
            toastStore.trigger(t);
        } else {
            updateInformation($user)
            .then(response => {
                if (response.status == 404) {
                    toastStore.trigger({
                        message: 'User not found',
                    });
                } else if (response.status == 401) {
                    toastStore.trigger({
                        message: 'Unauthorized',
                    });
                } else if (response.status == 200) {
                    toastStore.trigger({
                        message: 'Information updated successfully',
                    });
                }
            })
        }
    }
</script>

<Toast />

<div class="flex justify-center h-[100%]">
    <div class="flex flex-col m-[auto] {!isMobile ? 'w-[35%]': 'w-[80%]'} gap-[20px]">
        <label class="w-[100%] px-[10px]">
            <span>Username</span>
            <input class="input" type="text" placeholder="Username" bind:value={$user.username} readonly />
        </label>
                        
        <label class="w-[100%] px-[10px]">
            <span>Email</span>
            <input class="input" type="text" placeholder="Email" bind:value={$user.email} readonly />
        </label>
                
        <div class="flex">
            <label class="w-[100%] px-[10px]">
                <span>Name</span>
                <input class="input" type="text" placeholder="Name" bind:value={$user.firstname} required />
            </label>
                            
            <label class="w-[100%] px-[10px]">
                <span>Surname</span>
                <input class="input" type="text" placeholder="Surname" bind:value={$user.lastname} required />
            </label>
        </div>
    
        <label class="w-[100%] px-[10px]">
            <span>County</span>
            <select class="select" bind:value={$user.county} required >
                {#each Object.keys($romaniaCities) as county}
                    <option selected={county === $user.county} value={county}>{county}</option>
                {/each}
            </select>
        </label>
    
        <label class="w-[100%] px-[10px]">
            <span>City</span>
            <select class="select" bind:value={$user.city} required >
                {#if $user?.county == ''}
                    <option value=''>{$user.city}</option>
                {:else if $romaniaCities[$user.county]}
                    {#each $romaniaCities[$user.county] as city}
                        <option value={city}>{city}</option>
                    {/each}
                {/if}
            </select>
        </label>

        <button type="button" class="btn w-[100%] mx-[auto] variant-filled" on:click={handleUpdateInformation}>Update Information</button>
    </div>	
</div>
