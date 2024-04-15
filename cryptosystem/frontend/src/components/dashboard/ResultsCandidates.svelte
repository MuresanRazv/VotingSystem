<script lang="ts">
    import { polls, type Candidate } from "../../stores/polls";

    export let candidates: Candidate[] = [];
    export let pollStatus: string = '';
</script>

<div class="flex w-[100%] gap-10">
    <div class="bg-surface-800 p-10 rounded-3xl w-[50%]">
        <h2>
            Candidates Statistics
        </h2>
        
        <div class="flex flex-row gap-10">
            {#each candidates as candidate}
                <div class="h-[max-content] p-2">
                    <h3>
                        {candidate.name}
                    </h3>
                    {#if candidate.tally}
                        <p>
                            {candidate.tally} {parseInt(candidate.tally) === 1 ? 'vote' : 'votes'}
                        </p>
                    {:else}
                        <p>
                            No votes
                        </p>
                    {/if}
                </div>
            {/each}
        </div>
    </div>
    <div class="flex flex-col gap-5 bg-surface-800 p-10 rounded-3xl w-[50%]">
        <h2>
            {#if pollStatus}
                {#if pollStatus == 'in_progress'}
                    Poll Status: <strong 
                        class="text-yellow-500">
                        In Progress
                    </strong>
                {:else}
                    Poll Status: <strong 
                        class="text-green-500">
                        {pollStatus[0].toUpperCase() + pollStatus.slice(1)}
                    </strong>
                {/if}
            {:else}
                Poll Status: <strong class="text-red-500">Not available</strong>
            {/if}
        </h2>
        {#if pollStatus}
            {#if pollStatus == 'completed' || pollStatus == 'in_progress'}
                <button class="btn btn-primary variant-filled w-[max-content]" disabled={pollStatus != 'completed'}>
                    Publish Results
                </button>
            {:else if pollStatus == 'published'}
                <p>Results are published.</p>
            {/if}
        {/if}
    </div>
</div>
