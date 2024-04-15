<script lang="ts">
	import { SlideToggle, getModalStore, getToastStore, type ToastSettings, Toast } from "@skeletonlabs/skeleton";
    import { polls, type Poll } from "../../stores/polls";
    import { createPoll, getUserPolls, removePoll, updatePoll } from "../../helper/polls";

    const toastStore = getToastStore();
    const updated: ToastSettings = {
	    message: 'Poll updated successfully',
    };
    const created: ToastSettings = {
        message: 'Poll created successfully',
    };
    const deleted: ToastSettings = {
        message: 'Poll deleted successfully',
    };
    
    const modalStore = getModalStore();

    export let poll: Poll;
    export let canEdit: boolean;

    if (poll.start_date && poll.end_date) {
        poll.start_date = poll.start_date.split('T')[0];
        poll.end_date = poll.end_date.split('T')[0];
    }

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

    function validCandidates() {
        if (!poll.candidates) {
            return false;
        }
        return poll.candidates.every((candidate) => candidate.name && candidate.description);
    }

    function handleSave() {
        if (!poll.title || !poll.description || !validCandidates()) {
            return;
        }
        // Poll exists
        if (poll._id) {
            updatePoll(poll)
            .then((response) => {
                if (response.ok) {
                    modalStore.close();
                }
            })
            .then(() => {
                $polls = getUserPolls();
                toastStore.trigger(updated);
            });
        } else {
            // Create poll
            createPoll(poll)
            .then((response) => {
                if (response.ok) {
                    modalStore.close();
                }
            })
            .then(() => {
                $polls = getUserPolls();
                toastStore.trigger(created);
            });
        }
    }

    function handleDelete() {
        if (poll._id) {
            removePoll(poll._id)
            .then((response) => {
                if (response.ok) {
                    modalStore.close();
                }
            })
            .then(() => {
                $polls = getUserPolls();
                toastStore.trigger(deleted);
            });
        }
    }
</script>

<div class="card max-h-[80vh] w-[80%] p-10 flex flex-col gap-5 overflow-auto">
    <label class="label">
        <span>Title</span>
        <input class="input {!poll.title ? 'input-warning': ''}" type="text" placeholder="Name" bind:value={poll.title} />
    </label>
    
    <label class="label">
        <span>Description</span>
        <input class="input {!poll.description ? 'input-warning': ''}" type="text" placeholder="Description" bind:value={poll.description} />
    </label>
    
    <SlideToggle name="slider-medium" bind:checked={poll.multiple_choice} active="bg-primary-500" size="sm">Multiple-Choice</SlideToggle>

    <SlideToggle name="slider-medium" bind:checked={poll.is_private} active="bg-primary-500" size="sm">Private</SlideToggle>

    
    <span>Candidates</span>

    {#if poll.candidates && poll.candidates.length > 0}
        {#each poll.candidates as candidate, i}
            <div class="flex gap-5">
                <input class="input {!candidate.name ? 'input-warning': ''}" type="text" placeholder="Name" bind:value={candidate.name} readonly={!canEdit} required />
                <input class="input {!candidate.description ? 'input-warning': ''}" type="text" placeholder="Description" bind:value={candidate.description} readonly={!canEdit} required />
                {#if canEdit}
                    <button class="btn variant-filled-warning" on:click={() => removeCandidate(i)}>Remove</button>
                {/if}                
            </div>
        {/each}
    {/if}

    {#if canEdit}
        <button class="btn btn-primary variant-soft-surface" on:click={appendCandidate}>
            <img src="./plus-solid.svg" alt="plus" class="w-5 h-5"/>
        </button>
    {/if}

    <label class="label">
        <span>Start Date</span>
        <input type="date" class="input" readonly={!canEdit} bind:value={poll.start_date} />
    </label>
    
    <label class="label">
        <span>End Date</span>
        <input type="date" class="input" readonly={!canEdit} bind:value={poll.end_date} />
    </label>

    <div class="flex justify-between">
        <button class="btn btn-primary variant-filled-warning w-[max-content]" on:click={handleDelete}>
            Delete
        </button>
    
        <button class="btn btn-primary variant-filled w-[max-content]" on:click={handleSave}>
            Save
        </button>
    </div>
</div>