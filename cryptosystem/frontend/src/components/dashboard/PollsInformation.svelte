<script lang="ts">
    import { getGeneralResults, getResults } from "../../helper/polls";
    import '@carbon/charts-svelte/styles.css'
    import { browser } from '$app/environment';
    import { BarChartSimple } from '@carbon/charts-svelte'
    // TODO: get the polls statistics from the backend
    // go through each user poll and get the results, just display all of them initially
    // after implementing results, display them conditionally, maybe in a modal or a dropdown or something
    // also make endpoints for general statistics of all polls, or maybe top polls by votes and etc

    let data = []

    getGeneralResults()
    .then((results) => {
        
    })
</script>

<style>
    .polls-container {
        display: flex;
        flex-direction: row;
        height: 100%;
    }

    .votes-chart {
        display: flex;
        width: 60%;
        height: 100%;
    }

    .top-polls {
        display: flex;
        width: 40%;
        height: 100%;
    }
</style>

<div class="polls-container">
    <div class="votes-chart">

    </div>
    <div class="top-polls">

    </div>
</div>