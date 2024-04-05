<script lang="ts">
    import user from "../../stores/user";
    import romaniaCities from "../../stores/locations";
    import { Toast, getToastStore } from '@skeletonlabs/skeleton';
    import type { ToastSettings, ToastStore } from '@skeletonlabs/skeleton';
    import { initializeStores } from '@skeletonlabs/skeleton';
    import { goto } from "$app/navigation";
    import { register, login } from "../../helper/authentication";
    import { userToken } from "../../stores/user";

    initializeStores();
    const toastStore = getToastStore();
    const t: ToastSettings = {
	    message: 'Please fill all the fields',
    };
    const p: ToastSettings = {
        message: 'Passwords do not match',
    };

    let password = '';
    let confirmPassword = '';

    function handleRegister() {
        if ($user.firstname == '' || $user.lastname == '' || $user.county == '' || $user.county == '' || $user.email == '' || $user.username == '' || password == '') {
            toastStore.trigger(t);
        } else if (password !== confirmPassword) {
            toastStore.trigger(p);
        } else {
            register($user, password)
            .then(response => {
                if (response.status == 409) {
                    toastStore.trigger({
                        message: 'User already exists',
                    });
                } else if (response.status == 201) {
                    toastStore.trigger({
                        message: 'User created successfully',
                    });
                    goto('/dashboard');
                }
            })
            .then(data => {
                login($user.email, password)
                .then(data => {
                    localStorage.setItem('access_token', data.access_token)
                    $userToken
                    window.location.href = '/dashboard'
                    goto('/dashboard');
                })
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
        width: max-content;
        margin: 0 auto;
    }
</style>

<Toast />

<div class="user-information-container">
    <div class="user-information">
        <label class="label">
            <span>Username</span>
            <input class="input" type="text" placeholder="Username" bind:value={$user.username} required />
        </label>
                        
        <label class="label">
            <span>Email</span>
            <input class="input" type="text" placeholder="Email" bind:value={$user.email} required />
        </label>
                
        <label class="label">
            <span>Password</span>
            <input class='input {password !== confirmPassword ? "input-warning" : ""}' 
            type="password" placeholder="Password" bind:value={password} required />
        </label>

        <label class="label">
            <span>Confirm Password</span>
            <input class='input {password !== confirmPassword ? "input-warning" : ""}'
             type="password" placeholder="Confirm Password" bind:value={confirmPassword} required />
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

        <button type="button" class="btn variant-filled" on:click={handleRegister}>Register</button>
    </div>	
</div>
