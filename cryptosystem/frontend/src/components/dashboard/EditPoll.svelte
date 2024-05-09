<script lang="ts">
	import { SlideToggle, getModalStore, getToastStore, type ToastSettings, Toast } from "@skeletonlabs/skeleton";
    import { polls, type Poll } from "../../stores/polls";
    import { createPoll, getUserPolls, removePoll, updatePoll } from "../../helper/polls";
    import isMobileStore from "../../stores/generalStore";

    let isMobile = false;
    let loading = false;

    isMobileStore.subscribe(value => {
        isMobile = value;
    });

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
        return poll.candidates.every((candidate) => candidate.name);
    }

    function handleSave() {
        if (!poll.title || !poll.description || !validCandidates()) {
            return;
        }
        loading = true;

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
            })
            .finally(() => {
                loading = false;
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
            })
            .finally(() => {
                loading = false;
            });
        }
    }

    function handleDelete() {
        if (poll._id) {
            loading = true;
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
    {#if loading}
        <img src="./tube-spinner.svg" alt="Loading Spinner" class="absolute w-14 h-14 z-[9999]">
        <p class="absolute z-[9999] top-[54%]">{!poll._id ? 'Creating your poll...' : 'Updating your poll...'}</p>
    {/if}
<div class="card max-h-[80vh] {!isMobile ? 'p-10 w-[80%]': 'p-5 w-[95%]'} flex flex-col gap-5 overflow-auto {loading ? 'blur-sm pointer-events-none': ''}">
    <label class="label">
        <span>Title</span>
        <input class="input {!poll.title ? 'input-warning': ''}" type="text" placeholder="Name" bind:value={poll.title} />
    </label>
    
    <label class="label">
        <span>Description</span>
        <input class="input {!poll.description ? 'input-warning': ''}" type="text" placeholder="Description" bind:value={poll.description} />
    </label>
    
    <SlideToggle name="slider-medium" bind:checked={poll.multiple_choice} active="bg-primary-500" size="sm" disabled={!canEdit}>Multiple-Choice</SlideToggle>

    <SlideToggle name="slider-medium" bind:checked={poll.is_private} active="bg-primary-500" size="sm" disabled={!canEdit}>Private</SlideToggle>

    
    <span>Candidates</span>

    {#if poll.candidates && poll.candidates.length > 0}
        {#each poll.candidates as candidate, i}
            <div class="flex {!isMobile ? 'gap-5': 'gap-1'}">
                <input class="input {!candidate.name ? 'input-warning': ''}" type="text" placeholder="Name" bind:value={candidate.name} readonly={!canEdit} required />
                {#if canEdit}
                    {#if !isMobile}
                        <button class="btn variant-filled-warning" on:click={() => removeCandidate(i)}>Remove</button>
                    {:else}
                        <button class="btn variant-filled-warning" on:click={() => removeCandidate(i)}>
                            <img src="./trash-can-solid.svg" alt="trash" class="w-5 h-5"/>
                        </button>
                    {/if}
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