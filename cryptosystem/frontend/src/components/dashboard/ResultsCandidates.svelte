<script lang="ts">
    import { polls, type Candidate, type PollResults } from "../../stores/polls";
    import { publishPoll } from "../../helper/polls";
    import { Toast } from "@skeletonlabs/skeleton";
    import type { ToastSettings } from "@skeletonlabs/skeleton";
    import { getToastStore } from "@skeletonlabs/skeleton";

    export let results: PollResults | Promise<PollResults>;
    export let isMobile: Boolean;

    const toastStore = getToastStore();
    const published: ToastSettings = {
	    message: 'Poll updated successfully',
    };
    const failed: ToastSettings = {
        message: 'Failed to publish results',
    };

    function handlePublishResults(pollId: string, pollStatus: string) {
        publishPoll(pollId)
        .then((response) => {
            if (response.status === 200) {
                pollStatus = 'published';
                toastStore.trigger(published);
            } else {
                toastStore.trigger(failed);
            }
        })
    }
</script>

<Toast />

{#await results}
    <div class="placeholder animate-pulse" />
{:then results}
    {#if results.candidates.length > 0}
        <div class="flex {isMobile ? 'flex-col': '' } w-[100%] gap-5">
            <div class="bg-surface-800 p-10 rounded-3xl {!isMobile ? 'w-[50%]': '' }">
                <h2>
                    Candidates Statistics
                </h2>
                
                <div class="flex flex-row gap-10">
                    {#each results.candidates as candidate}
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
            <div class="flex flex-col gap-5 bg-surface-800 p-10 rounded-3xl {!isMobile ? 'w-[50%]': '' }">
                <h2>
                    {#if results.status}
                        {#if results.status == 'in_progress'}
                            Poll Status: <strong 
                                class="text-yellow-500">
                                In Progress
                            </strong>
                        {:else if results.status == 'pending'}
                            Poll Status: <strong 
                                class="text-blue-500">
                                Pending
                            </strong>
                        {:else}
                            Poll Status: <strong 
                                class="text-green-500">
                                {results.status[0].toUpperCase() + results.status.slice(1)}
                            </strong>
                        {/if}
                    {:else}
                        Poll Status: <strong class="text-red-500">Not available</strong>
                    {/if}
                </h2>
                {#if results.status}
                    {#if results.status == 'completed' || results.status == 'in_progress'}
                        <button class="btn btn-primary variant-filled w-[max-content]" disabled={results.status != 'completed'} on:click={() => {if (results._id) {handlePublishResults(results._id, results.status)}}}>
                            Publish Results
                        </button>
                    {:else if results.status == 'published'}
                        <p>Results are published.</p>
                    {/if}
                {/if}
            </div>
        </div>
    {/if}
{/await}