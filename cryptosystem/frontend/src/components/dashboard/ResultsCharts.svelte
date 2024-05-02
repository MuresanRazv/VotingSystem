<script lang="ts">
    import { BarChartSimple, PieChart } from "@carbon/charts-svelte";
    import type { PollResults } from "../../stores/polls";

    export let showBarChart: boolean;
    export let results: PollResults | Promise<PollResults>;
    export let isMobile: boolean;
</script>

{#await results}
    {#if showBarChart}
        <div class="bg-surface-800 h-[max-content] w-[60%] rounded-3xl p-5">
            <BarChartSimple data={[]} options={{
                title: 'Votes This Week',
                axes: {
                    left: {
                        mapsTo: 'value'
                    },
                    bottom: {
                        mapsTo: 'group',
                        // @ts-ignore
                        scaleType: 'labels'
                    }
                },
                height: '400px',
                width: '100%',
                resizable: true,
                theme: "g100",
            }} />
        </div>
    {/if}
    <div class="bg-surface-800 h-[max-content] {!showBarChart ? 'w-[100%]': 'w-[40%]'} rounded-3xl p-5">
        <PieChart data={[]} options={{
            title: 'County Statistics',
            height: '400px',
            width: '100%',
            resizable: true,
            legend: {
                position: 'bottom'
            },
            theme: "g100"
        }} />
    </div>
{:then results}
    {#if showBarChart}
        <div class="bg-surface-800 h-[max-content] {!isMobile ? 'w-[60%]': '' } rounded-3xl p-5">
            <BarChartSimple data={Object.entries(results.votes_this_week).map(([key, value]) => {
                return {
                    group: key,
                    value: value
                }
            })} options={{
                title: 'Votes This Week',
                axes: {
                    left: {
                        mapsTo: 'value'
                    },
                    bottom: {
                        mapsTo: 'group',
                        // @ts-ignore
                        scaleType: 'labels'
                    }
                },
                height: '400px',
                width: '100%',
                resizable: true,
                theme: "g100",
            }} />
        </div>
    {/if}
    <div class="bg-surface-800 h-[max-content] {!showBarChart || isMobile ? 'w-[100%]': 'w-[40%]'} rounded-3xl p-5">
        <PieChart data={Object.entries(results.county_statistics).map(([key, value]) => {
            return {
                group: key,
                value: value
            }
        })} options={{
            title: 'County Statistics',
            height: '400px',
            width: '100%',
            resizable: true,
            legend: {
                position: 'bottom'
            },
            theme: "g100"
        }} />
    </div>
{/await}