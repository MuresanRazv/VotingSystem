<script lang="ts">
    import user from "../stores/user";
    import romaniaCities from "../stores/locations"; 
    import { Toast, getToastStore } from '@skeletonlabs/skeleton';
    import type { ToastSettings, ToastStore } from '@skeletonlabs/skeleton';
    import { initializeStores } from '@skeletonlabs/skeleton';

    initializeStores();
    const toastStore = getToastStore();
    const t: ToastSettings = {
	    message: 'Please fill all the fields',
    };

    function updateInformation() {
        if ($user.firstname == '' || $user.lastname == '' || $user.county == '' || $user.county == '') {
            toastStore.trigger(t);
        } else {
            fetch(`http://127.0.0.1:8000/api/users/${$user._id}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify({
                    firstname: `${$user.firstname}`,
                    lastname: `${$user.lastname}`,
                    county: `${$user.county}`,
                    city: `${$user.city}`
                })
            })
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

<style>
    .user-information {
        display: flex;
        flex-direction: column;
        margin: auto;
        width: 35%;
        gap: 20px;
    }

    .form-group {
        display: flex;
        flex-direction: row;
    }

    .label {
        width: 100%;
        padding: 0 10px;
    }

    .user-information-container {
        display: flex;
        justify-content: center;
        height: 100%;
    }

    .btn {
        width: 25%;
        margin: 0 auto;
    }
</style>

<Toast />

<div class="user-information-container">
    <div class="user-information">
        <label class="label">
            <span>Username</span>
            <input class="input" type="text" placeholder="Username" bind:value={$user.username} readonly />
        </label>
                        
        <label class="label">
            <span>Email</span>
            <input class="input" type="text" placeholder="Email" bind:value={$user.email} readonly />
        </label>
                
        <div class="form-group">
            <label class="label">
                <span>Name</span>
                <input class="input" type="text" placeholder="Name" bind:value={$user.firstname} required />
            </label>
                            
            <label class="label">
                <span>Surname</span>
                <input class="input" type="text" placeholder="Surname" bind:value={$user.lastname} required />
            </label>
        </div>
    
        <label class="label">
            <span>County</span>
            <select class="select" bind:value={$user.county} required >
                {#each Object.keys($romaniaCities) as county}
                    <option selected={county === $user.county} value={county}>{county}</option>
                {/each}
            </select>
        </label>
    
        <label class="label">
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

        <button type="button" class="btn variant-filled" on:click={updateInformation}>Update Information</button>
    </div>	
</div>
