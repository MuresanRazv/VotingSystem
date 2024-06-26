<script lang="ts">
	import { onMount } from "svelte";
    import type { Poll } from "../../stores/polls";
	import user from "../../stores/user";
	import type { Vote } from "../../stores/votes";
	import { addVote } from "../../helper/votes";
	import { getModalStore, getToastStore, type ToastSettings } from "@skeletonlabs/skeleton";
    import { polls } from "../../stores/polls";
    import { votes } from "../../stores/votes";
    import { getPublicPolls } from "../../helper/polls";
    import { getUserVotes } from "../../helper/votes";

    const modalStore = getModalStore();
    const toastStore = getToastStore();
    const submittedVote: ToastSettings = {
	    message: 'Vote submitted successfully. Thank you for participating! 🎉',
    };
    const errorVote: ToastSettings = {
        message: 'There was an error submitting your vote. Please try again.',
    };

    export let poll: Poll;
    let inputType = poll.multiple_choice ? 'checkbox' : 'radio';

    let vote: Vote = {
        poll_id: poll._id ? poll._id : '',
        candidates: poll.candidates,
        user_id: $user._id ? $user._id : ''
    }

    let loading = false;

    onMount(() => {
        // Initialize tallies
        vote.candidates.forEach(candidate => {
            candidate.tally = '0';
        });
    });

    function handleSubmitVote() {
        if (poll._id) {
            loading = true;
            addVote(poll._id, vote)
            .then((response) => {
                $polls = getPublicPolls();
                $votes = getUserVotes($user._id);
                modalStore.close();
                return response;
            })
            .then((response) => {
                if (response.ok) {
                    toastStore.trigger(submittedVote);
                } else {
                    toastStore.trigger(errorVote);
                }
            })
            .finally(() => {
                loading = false;
            })
        }
    }

    function handleChooseCandidate(index: number) {
        if (inputType === 'radio') {
            vote.candidates.forEach((candidate, i) => {
                if (i === index) {
                    candidate.tally = '1';
                } else {
                    candidate.tally = '0';
                }
            });
        } else {
            vote.candidates[index].tally = vote.candidates[index].tally === '1' ? '0' : '1';
        }
    }
</script>

{#if loading}
    <img src="./tube-spinner.svg" alt="Loading Spinner" class="absolute w-14 h-14 z-[9999]">
    <p class="absolute z-[9999] top-[54%]">Adding your vote...</p>
{/if}
<div class="card max-h-[80vh] w-[80%] p-10 flex flex-col gap-5 overflow-auto {loading ? 'blur-sm pointer-events-none': ''}">
    <h3>{poll.title}</h3>
    <p>{poll.description}</p>
    <form>
        {#each poll.candidates as candidate, i}
            <div class="space-y-2">
                <label class="flex items-center space-x-2">
                    <input class="{inputType}" type="{inputType}" id="{String(i)}" name="candidate" value="{candidate.name}" on:change={() => {
                        handleChooseCandidate(i);
                    }} />
                    <p>{candidate.name}</p>
                </label>
            </div>
        {/each}
    </form>
    <button class="btn btn-primary variant-filled w-[max-content]" on:click={handleSubmitVote} >Submit Vote</button>
</div>