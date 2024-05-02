<script lang="ts">
	import SvgQR from '@svelte-put/qr/svg/QR.svelte';
    import { clipboard } from '@skeletonlabs/skeleton';
    
    export let poll_code: string;
    export let poll_id: string;
    export let isMobile: boolean;

    const poll_link = poll_code ? `http://localhost:5173/dashboard?poll_code=${poll_code}`: `http://localhost:5173/dashboard?poll_id=${poll_id}`;
    const poll_logo = '../privacy-document-icon.svg';
    let show_link_copied = false;

    function setFlagTrueForSeconds() {
        show_link_copied = true;
        setTimeout(() => {
            show_link_copied = false;
        }, 2000);
    }
</script>

<div class="{isMobile ? 'w-[80%]': 'w-[30%]'} max-h-[80vh] overflow-scroll bg-surface-800 p-10 rounded-3xl">
    <div class="flex flex-col justify-center mx-[auto] text-center gap-[20px]">
        {#if poll_code}
            <span>Your private poll code:</span>
            <button class="variant-soft rounded-3xl p-2" use:clipboard={poll_link} on:click={setFlagTrueForSeconds}>
                <h2 class="h2">
                    {poll_code}
                </h2>
            </button>
        {:else}
            <span>Your public poll link:</span>
            <button class="truncate variant-soft max-w-[95%] rounded-3xl p-2" use:clipboard={poll_link} on:click={setFlagTrueForSeconds}>
                {poll_link}
            </button>
        {/if}
        
        {#if show_link_copied}
            <small>Link copied!</small>
        {/if}
        <SvgQR data={poll_link} logo={poll_logo} />
    </div>
</div>