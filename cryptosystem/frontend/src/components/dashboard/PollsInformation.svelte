<script lang="ts">
    import { getGeneralResults, getResults, getUserPolls } from "../../helper/polls";
    import '@carbon/charts-svelte/styles.css'
    import { browser } from '$app/environment';
    import ResultsCharts from "./ResultsCharts.svelte";
    import ResultsCandidates from "./ResultsCandidates.svelte";
    import { Autocomplete } from '@skeletonlabs/skeleton';
    import type { AutocompleteOption, PopupSettings } from '@skeletonlabs/skeleton';
    import { popup } from "@skeletonlabs/skeleton";
	import { polls, type Poll } from "../../stores/polls";

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

<div class="flex flex-col m-10 gap-10">
    <div class="flex w-[30%]">
        <div class="w-[90%]">
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
        </div>
        <div>
            <button on:click={() => {searchInput = ''; results=getGeneralResults();}} class="btn btn-primary variant-soft-surface mt-0.5 ml-2 p-3 {searchInput !== '' ? 'visible opacity-100': 'invisible opacity-0'} transition ease-in-out delay-150" >
                <img src="./x-solid.svg" class="w-3 h-3" alt="Clear text" />
            </button>
        </div>
        <div data-popup="popupAutocomplete" class="bg-surface-900 p-2 rounded-3xl z-[9999]">
            <Autocomplete
                bind:input={searchInput}
                options={searchOptions}
                on:selection={onInputSelection}
            />
        </div>
    </div>

    <div class="flex w-[100%] h-[100%] gap-10">                                
        <ResultsCharts {results} showBarChart={true} />
    </div>
    <ResultsCandidates {results} />


</div>