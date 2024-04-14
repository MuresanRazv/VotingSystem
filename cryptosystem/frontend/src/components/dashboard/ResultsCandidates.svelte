<script lang="ts">
    import type { Candidate } from "../../stores/polls";

    export let candidates: Candidate[] = [];
</script>

<h2>
    Candidates Statistics
</h2>

<div class="flex flex-row gap-10">
    {#each candidates as candidate}
        <div class="bg-surface-900 h-[max-content] rounded-3xl p-5">
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