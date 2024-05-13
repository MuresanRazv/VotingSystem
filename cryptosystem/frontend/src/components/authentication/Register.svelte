<script lang="ts">
    import user from "../../stores/user";
    import romaniaCities from "../../stores/locations";
    import { Toast, getToastStore } from '@skeletonlabs/skeleton';
    import type { ToastSettings, ToastStore } from '@skeletonlabs/skeleton';
    import { initializeStores } from '@skeletonlabs/skeleton';
    import { goto } from "$app/navigation";
    import { register, login } from "../../helper/authentication";
    import { userToken } from "../../stores/user";
    import isMobileStore from "../../stores/generalStore";

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
    let isMobile = false;

    isMobileStore.subscribe(value => {
        isMobile = value;
    });

    let loading = false;

    function handleRegister() {
        if ($user.firstname == '' || $user.lastname == '' || $user.county == '' || $user.county == '' || $user.email == '' || $user.username == '' || password == '') {
            toastStore.trigger(t);
        } else if (password !== confirmPassword) {
            toastStore.trigger(p);
        } else {
            loading = true;
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
            .finally(() => {
                loading = false;
            })
        }
    }
</script>

<Toast />

<div class="flex flex-col justify-center h-[100%] py-5">
    <header class="text-center pt-5 py-10">
        <h2 class="h2">
            Register
        </h2>
    </header>

    <div class="flex flex-col m-[auto] {!isMobile ? 'w-[35%]': 'w-[70%]'} gap-[20px]">
        <label class="w-[100%] p-[0 10px]">
            <span>Username</span>
            <input class="input" type="text" placeholder="Username" bind:value={$user.username} required />
        </label>
                        
        <label class="w-[100%] p-[0 10px]">
            <span>Email</span>
            <input class="input" type="text" placeholder="Email" bind:value={$user.email} required />
        </label>
                
        <label class="w-[100%] p-[0 10px]">
            <span>Password</span>
            <input class='input {password !== confirmPassword ? "input-warning" : ""}' 
            type="password" placeholder="Password" bind:value={password} required />
        </label>

        <label class="w-[100%] p-[0 10px]">
            <span>Confirm Password</span>
            <input class='input {password !== confirmPassword ? "input-warning" : ""}'
             type="password" placeholder="Confirm Password" bind:value={confirmPassword} required />
        </label>

        <div class="flex gap-[5px]">
            <label class="w-[100%] p-[0 10px]">
                <span>Name</span>
                <input class="input" type="text" placeholder="Name" bind:value={$user.firstname} required />
            </label>
                            
            <label class="w-[100%] p-[0 10px]">
                <span>Surname</span>
                <input class="input" type="text" placeholder="Surname" bind:value={$user.lastname} required />
            </label>
        </div>
    
        <label class="w-[100%] p-[0 10px]">
            <span>County</span>
            <select class="select" bind:value={$user.county} required >
                {#each Object.keys($romaniaCities) as county}
                    <option selected={county === $user.county} value={county}>{county}</option>
                {/each}
            </select>
        </label>
    
        <label class="w-[100%] p-[0 10px]">
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

        <button type="button" class="btn variant-filled-secondary" disabled={loading} on:click={handleRegister}>
            {#if loading}
                <img src="./tube-spinner.svg" alt="Loading Spinner" class="w-6 h-6">
                Creating your account...
            {:else}
                Register
            {/if}
        </button>
    </div>	
</div>
