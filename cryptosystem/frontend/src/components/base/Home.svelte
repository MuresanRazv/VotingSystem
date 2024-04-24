<script lang="ts">
	import { RadioGroup, RadioItem } from "@skeletonlabs/skeleton";
    import { browser } from "$app/environment";
	import { onMount } from "svelte";

    let value: number = 0;
    let isMobile = false;
    let rounded = isMobile ? 'rounded-lg': 'rounded-3xl';
    let padding = isMobile ? 'p-5': 'p-2';

    onMount(() => {
        window.addEventListener('resize', () => {
            isMobile = window.innerWidth < 768;
            rounded = isMobile ? 'rounded-lg': 'rounded-3xl';
            padding = isMobile ? 'p-5': 'p-2';
        });
    });
</script>

<div class="mx-[auto] p-10 text-center max-w-[900px] flex flex-col gap-10">
    <h1 class="h1 font-bold">Welcome to CyberPolls!</h1>

    <RadioGroup background="bg-secondary-800" border="border-0" flexDirection="{isMobile ? 'flex-col': 'flex-row'}" rounded={rounded}>
        <RadioItem rounded={rounded} padding={padding} bind:group={value} name="justify" value={0}>What is CyperPolls?</RadioItem>
        <RadioItem rounded={rounded} padding={padding} bind:group={value} name="justify" value={1}>How do I create polls?</RadioItem>
        <RadioItem rounded={rounded} padding={padding} bind:group={value} name="justify" value={2}>How do I share/join polls?</RadioItem>
    </RadioGroup>

    <div id="displayHelp" class="flex flex-col gap-5 rounded-3xl bg-secondary-800 p-10">
        {#if value === 0}
            <p class="text-lg">CyberPolls is your go-to for online polls done right. With top-notch security using the Paillier cryptosystem, it guarantees privacy while you share opinions, gather insights, and explore trends. Join the community and make your voice count with CyberPolls.</p>
        {/if}

        {#if value === 1}
            <p class="text-lg">To create polls, first, you'll need to sign up for an account. Once you're logged in, head over to your dashboard. There, you'll find the 'Manage Polls' tab. Click on it, and you'll see a plus button – hit that to start creating your poll. It's that simple! Start engaging and gathering insights with your custom polls on CyberPolls.</p>
        {/if}

        {#if value === 2}
            <p class="text-lg">To share polls, navigate to the 'Manage Polls' tab in your dashboard and select 'Share.' You can then copy a link or use a QR code for easy distribution.</p>
            <p class="text-lg">Joining polls is straightforward. For public polls, simply click on a shared link or locate them in the 'Polls' tab of your dashboard. For private polls, enter the provided code or utilize an invitation link/QR code. Start voting seamlessly with CyberPolls.</p>
        {/if}
    </div>
</div>