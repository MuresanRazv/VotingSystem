<script lang="ts">
    import user from "../stores/user";
    import romaniaCities from "../stores/locations"; 
    import { Toast, getToastStore } from '@skeletonlabs/skeleton';
    import type { ToastSettings, ToastStore } from '@skeletonlabs/skeleton';
    import { initializeStores } from '@skeletonlabs/skeleton';
	import { afterUpdate } from "svelte";
    import { userToken } from "../stores/user";

    initializeStores();
    const toastStore = getToastStore();
    const t: ToastSettings = {
	    message: 'Please fill all the fields',
    };
    
    let selectedCounty = '';
    let selectedCity = '';
    let name = $user?.full_name.split(" ")[0];
    let surname = $user?.full_name.split(" ").slice(1).join(" ");

    afterUpdate(() => {
        name = $user?.full_name.split(" ")[0];
        surname = $user?.full_name.split(" ").slice(1).join(" ");
    });

    function updateInformation() {
        if (name == '' || surname == '' || selectedCounty == '' || selectedCity == '') {
            toastStore.trigger(t);
        } else {
            fetch(`http://127.0.0.1:8000/api/users/${$user?.email}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify({
                    full_name: `${name} ${surname}`,
                    address: `${selectedCity}, ${selectedCounty}`,
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
            console.log(name, surname, selectedCounty, selectedCity);
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
            <input class="input" type="text" placeholder="Username" value={$user?.username} readonly />
        </label>
                        
        <label class="label">
            <span>Email</span>
            <input class="input" type="text" placeholder="Email" value={$user?.email} readonly />
        </label>
                
        <div class="form-group">
            <label class="label">
                <span>Name</span>
                <input class="input" type="text" placeholder="Name" bind:value={name} required />
            </label>
                            
            <label class="label">
                <span>Surname</span>
                <input class="input" type="text" placeholder="Surname" bind:value={surname} required />
            </label>
        </div>
    
        <label class="label">
            <span>County</span>
            <select class="select" bind:value={selectedCounty} required >
                {#each Object.keys($romaniaCities) as county}
                    <option value={county}>{county}</option>
                {/each}
            </select>
        </label>
    
        <label class="label">
            <span>City</span>
            <select class="select" bind:value={selectedCity} required >
                {#if selectedCounty == ''}
                    <option value=''>Select a county first</option>
                {:else}
                    {#each $romaniaCities[selectedCounty] as city}
                        <option value={city}>{city}</option>
                    {/each}
                {/if}
            </select>
        </label>

        <button type="button" class="btn variant-filled" on:click={updateInformation}>Update Information</button>
    </div>	
</div>
