<script lang="ts">
    import { getGeneralResults, getResults } from "../../helper/polls";
    import '@carbon/charts-svelte/styles.css'
    import { browser } from '$app/environment';
    import { BarChartSimple, PieChart } from '@carbon/charts-svelte'
    // TODO: get the polls statistics from the backend
    // go through each user poll and get the results, just display all of them initially
    // after implementing results, display them conditionally, maybe in a modal or a dropdown or something
    // also make endpoints for general statistics of all polls, or maybe top polls by votes and etc

</script>

<style>
    .top-polls {
        display: flex;
        width: 40%;
        height: 100%;
    }
</style>

<div class="flex flex-row h-[100%]">
    <div class="flex w-[60%] h-[100%]">
        {#await getGeneralResults()}
            <p>Loading...</p>
        {:then results}
            {#if results}
                <div class="m-10 bg-surface-900 h-[max-content] rounded-3xl p-5">
                    <PieChart data={Object.entries(results.county_statistics).map(([key, value]) => {
                        return {
                            group: key,
                            value: value
                        }
                    })} options={{
                        title: 'County Statistics',
                        height: '400px',
                        width: '400px',
                        resizable: true,
                        legend: {
                            position: 'bottom'
                        },
                        theme: "g100"
                    }} />
                </div>
                <div class="m-10 bg-surface-900 h-[max-content] rounded-3xl p-5">
                    <BarChartSimple data={Object.entries(results.votes_this_week).map(([key, value]) => {
                        return {
                            date: new Date(key),
                            group: 'Votes This Week',
                            value: value
                        }
                    })} options={{
                        title: 'Votes This Week',
                        axes: {
                            left: {
                            mapsTo: 'value'
                            },
                            bottom: {
                            mapsTo: 'date',
                    
                            }
                        },
                        height: '400px'
                    }} />
                </div>
            {/if}
        {/await}
    </div>
    <div class="top-polls">

    </div>
</div>