<script lang="ts">
	import { RadioGroup, RadioItem } from "@skeletonlabs/skeleton";
    import { browser } from "$app/environment";
	import { onMount } from "svelte";
    import isMobileStore from "../../stores/generalStore";

    let value: number = 0;
    let isMobile = false;
    let rounded = isMobile ? 'rounded-lg': 'rounded-3xl';
    let padding = isMobile ? 'p-5': 'p-2';

    isMobileStore.subscribe(value => {
        isMobile = value;
        rounded = isMobile ? 'rounded-lg': 'rounded-3xl';
        padding = isMobile ? 'p-5': 'p-2';
    });
</script>

<div class="mx-[auto] p-10 text-center max-w-[900px] flex flex-col gap-10">
    <h1 class="h1 font-bold">Welcome to CyberPolls!</h1>

    <RadioGroup background="bg-secondary-800" border="border-0" flexDirection="{isMobile ? 'flex-col': 'flex-row'}" rounded={rounded}>
        <RadioItem rounded={rounded} padding={padding} bind:group={value} name="justify" value={0}>What is CyperPolls?</RadioItem>
        <RadioItem rounded={rounded} padding={padding} bind:group={value} name="justify" value={1}>What is the Paillier Cryptosystem?</RadioItem>
        <RadioItem rounded={rounded} padding={padding} bind:group={value} name="justify" value={2}>What can I do on this platform?</RadioItem>
    </RadioGroup>

    <div id="displayHelp" class="flex flex-col gap-5 rounded-3xl bg-secondary-800 p-10 text-left">
        {#if value === 0}
            <div class="flex {isMobile ? 'flex-col': ''} gap-10">
                <div class="flex gap-5 flex-col {!isMobile ? 'w-[70%]': ''}">
                    <h2 class="h2">Advanced Voting</h2>
                    <p class="text-lg">CyberPolls is an online voting platform which uses the Paillier Cryptosystem to encrypt your polls/votes, keeping your data secure.</p>
                </div>
                <img src="./user-shield-solid.svg" alt="check-to-slot" class="{!isMobile ? 'w-[30%]': 'w-[100%]'}" >
            </div>
        {/if}

        {#if value === 1}
            <div class="flex {isMobile ? 'flex-col': ''} gap-10">
                <div class="flex gap-5 flex-col {!isMobile ? 'w-[70%]': ''}">
                    <h2 class="h2">Secure Voting</h2>
                    <p class="text-lg">The Paillier Cryptosystem is an homomorphic encryption system. Due to its additive properties, your vote is kept encrypted on the server <strong>permanently</strong> and can only be decrypted by the creator of the poll.</p>
                </div>
                <img src="./check-to-slot-solid.svg" alt="check-to-slot" class="{!isMobile ? 'w-[30%]': 'w-[100%]'}" >
            </div>
        {/if}

        {#if value === 2}
            <div class="flex {isMobile ? 'flex-col': ''} gap-10">
                <div class="flex gap-5 flex-col {!isMobile ? 'w-[70%]': ''}">
                    <h2 class="h2">Features</h2>
                    <p class="text-lg">Create as many polls as you like and make your opinions heard by voting on other people's polls. As a poll creator, you also have access to various statistics about your polls and can share them to your friends.</p>
                    <h2 class="h2">Want some privacy?</h2>
                    <p class="text-lg">You can also create private polls which are only accessible by sharing your poll code/QR code.</p>
                </div>
                <img src="./square-poll-vertical-solid.svg" alt="check-to-slot" class="{!isMobile ? 'w-[30%]': 'w-[100%]'}" >
            </div>
        {/if}
    </div>

    <h2 class="h2">Don't have an account?</h2>
    <a href="/register" class="btn btn-primary bg-secondary-800 w-[70%] mx-[auto]">Register here!</a>
</div>