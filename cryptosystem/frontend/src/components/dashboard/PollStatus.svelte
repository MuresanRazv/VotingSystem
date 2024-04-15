<script lang="ts">
	import { onMount } from "svelte";
    import { getResults } from "../../helper/polls";
    import ResultsCharts from "./ResultsCharts.svelte";
    import ResultsCandidates from "./ResultsCandidates.svelte";
	import type { PollResults } from "../../stores/polls";

    export let poll_id: string;
    let results: PollResults;
    let published = true;
    let winner = '';
    let status = '';

    onMount(() => {
        getResults(poll_id)
        .then((response: any) => {
            console.log(response)
            if (response.detail) {
                throw response.detail;
            }

            results = response;
            let mostVotes = 0;
            results.candidates.forEach((candidate) => {
                if (candidate.tally && parseInt(candidate.tally) > mostVotes) {
                    mostVotes = parseInt(candidate.tally);
                    winner = candidate.name;
                }
            })
        })
        .catch((error: any) => {
            published = false;
            status = error.status.split('_').join(' ');
            status = status.charAt(0).toUpperCase() + status.slice(1);
        });
    });
</script>

<div class="flex flex-col bg-surface-900 rounded-3xl p-10 gap-5">
    {#if published && results}
        <h3>🏆 Winner: {winner}</h3>
        <ResultsCharts {results} showBarChart={false} />
        <ResultsCandidates {results} />
    {:else}
        <p>Sorry, but the results have not been published by the creator of the poll.</p>
        <p>Status: <strong class="{status != 'Completed' ? 'text-yellow-500': 'text-green-500'}">{status}</strong></p>
    {/if}
</div>