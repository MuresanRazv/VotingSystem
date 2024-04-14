<script lang="ts">
    import { getGeneralResults, getResults, getUserPolls } from "../../helper/polls";
    import '@carbon/charts-svelte/styles.css'
    import { browser } from '$app/environment';
    import ResultsCharts from "./ResultsCharts.svelte";
    import ResultsCandidates from "./ResultsCandidates.svelte";
    import { Autocomplete } from '@skeletonlabs/skeleton';
    import type { AutocompleteOption, PopupSettings } from '@skeletonlabs/skeleton';
    import { popup } from "@skeletonlabs/skeleton";
	import type { Poll } from "../../stores/polls";

    let searchInput = '';
    let searchOptions: AutocompleteOption<string>[] = [];
    let popupSettings: PopupSettings = {
        event: 'focus-click',
        target: 'popupAutocomplete',
        placement: 'bottom',
    };
    getUserPolls().then((polls) => {
        searchOptions = polls.map((poll: Poll) => {
            return {
                value: poll.title,
                label: poll.title,
                id: poll._id    
            }
        });
    });
    function onInputSelection(event: CustomEvent<AutocompleteOption<string>>) {
        searchInput = event.detail.label;
        // @ts-ignore
        results = getResults(event.detail.id);
    }
    
    let results = getGeneralResults();
    
</script>

<div class="flex flex-col w-[100%] m-10 gap-10">
    <div class="w-[25%]">
        <input
            class="input autocomplete"
            type="search"
            name="autocomplete-search"
            bind:value={searchInput}
            on:input={() => {            
                if (searchInput === '') {
                    results = getGeneralResults();
                }
            }}
            placeholder="Search..."
            use:popup={popupSettings}
        />
        <div data-popup="popupAutocomplete" class="bg-surface-900 p-2 rounded-3xl z-[9999]">
            <Autocomplete
                bind:input={searchInput}
                options={searchOptions}
                on:selection={onInputSelection}
            />
        </div>
    </div>
    {#await results}
        <p>Loading...</p>
    {:then results}
        <div class="flex flex-row h-[100%]">
            <div class="flex w-[60%] h-[100%] gap-10">                                        
                <ResultsCharts {results} />            
            </div>
        </div>
        {#if results.candidates.length > 0}
            <ResultsCandidates candidates={results.candidates} />
        {/if}        
    {/await}
</div>