<script lang="ts">
	import { SlideToggle, getModalStore, getToastStore, initializeStores, type ToastSettings, Toast } from "@skeletonlabs/skeleton";
    import type { Poll } from "../helper/polls";
    import { updatePoll } from "../helper/polls";

    const toastStore = getToastStore();
    const t: ToastSettings = {
	    message: 'Poll updated successfully',
    };
    
    const modalStore = getModalStore();

    export let poll: Poll;

    function appendCandidate() {
        if (!poll.candidates) {
            poll.candidates = [];
        }
        poll.candidates = [...poll.candidates, {name: '', description: ''}];
    }

    function removeCandidate(i: number) {
        if (poll.candidates && poll.candidates.length > 0) {
            poll.candidates = poll.candidates.filter((_, index) => index !== i);
        } else {
            poll.candidates = [];
        }
    }

    function handleSave() {
        updatePoll(poll)
        .then((response) => {
            if (response.ok) {
                modalStore.close();
            }
        })
        .then(() => {
            toastStore.trigger(t);
        });
    }
</script>

<div class="card max-h-[80vh] w-[80%] p-10 flex flex-col gap-5 overflow-auto">
    <label class="label">
        <span>Title</span>
        <input class="input" type="text" placeholder="Name" bind:value={poll.title} />
    </label>
    
    <label class="label">
        <span>Description</span>
        <input class="input" type="text" placeholder="Description" bind:value={poll.description} />
    </label>
    
    <SlideToggle name="slider-medium" bind:checked={poll.multiple_choice} active="bg-primary-500" size="sm">Multiple-Choice</SlideToggle>

    <SlideToggle name="slider-medium" bind:checked={poll.is_private} active="bg-primary-500" size="sm">Private</SlideToggle>

    
    <span>Candidates</span>

    {#if poll.candidates && poll.candidates.length > 0}
        {#each poll.candidates as candidate, i}
            <div class="flex gap-5">
                <input class="input" type="text" placeholder="Name" bind:value={candidate.name} />
                <input class="input" type="text" placeholder="Description" bind:value={candidate.description} />
                <button class="btn btn-danger" on:click={() => removeCandidate(i)}>Remove</button>
            </div>
        {/each}
    {/if}

    <button class="btn btn-primary variant-soft-surface" on:click={appendCandidate}>
        <img src="./plus-solid.svg" alt="plus" class="w-5 h-5"/>
    </button>
    
    <button class="btn btn-primary variant-filled w-[max-content] ml-auto" on:click={handleSave}>
        Save
    </button>
</div>