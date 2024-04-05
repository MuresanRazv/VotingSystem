<script lang="ts">
	import { onMount } from "svelte";
    import type { Poll } from "../../stores/polls";
	import user from "../../stores/user";
	import type { Vote } from "../../stores/votes";
	import { addVote } from "../../helper/votes";

    export let poll: Poll;
    let inputType = poll.multiple_choice ? 'checkbox' : 'radio';

    let vote: Vote = {
        poll_id: poll._id ? poll._id : '',
        candidates: poll.candidates,
        user_id: $user._id ? $user._id : ''
    }

    onMount(() => {
        // Initialize tallies
        vote.candidates.forEach(candidate => {
            candidate.tally = '0';
        });
    });

    function handleSubmitVote() {
        if (poll._id) {
            addVote(poll._id, vote);
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

<div class="card max-h-[80vh] w-[80%] p-10 flex flex-col gap-5 overflow-auto">
    <h3>{poll.title}</h3>
    <p>{poll.description}</p>
    <form>
        {#each poll.candidates as candidate, i}
            <div class="space-y-2">
                <label class="flex items-center space-x-2">
                    <input class="{inputType}" type="{inputType}" id="{String(i)}" name="candidate" value="{candidate.name}" on:change={() => {
                        handleChooseCandidate(i);
                        console.log(vote);
                    }} />
                    <p>{candidate.name}</p>
                </label>
            </div>
        {/each}
    </form>
    <button class="btn btn-primary variant-filled w-[max-content]" on:click={handleSubmitVote} >Submit Vote</button>
</div>