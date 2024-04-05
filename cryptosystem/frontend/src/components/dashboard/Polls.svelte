<script lang="ts">
	import { getModalStore } from "@skeletonlabs/skeleton";
    import type { ModalComponent, ModalSettings } from '@skeletonlabs/skeleton';
	import { getPublicPolls } from "../../helper/polls";
    import { polls } from "../../stores/polls";
    import VotePoll from "./VotePoll.svelte";
    
    const modalStore = getModalStore();
    const modalComponent: ModalComponent = { ref: VotePoll };
    const modal: ModalSettings = {
        type: 'component',
        component: modalComponent,
    };

    $polls = getPublicPolls();
</script>

<div class="flex flex-row overflow-auto max-h-[65vh] m-10 gap-2">
    <div class="flex flex-row w-3/4 bg-surface-900 rounded-3xl">
        <div class="flex flex-col w-4/6 p-10 gap-5">
            <h3>Public polls</h3>
            {#await $polls}
                <p>Loading...</p>
            {:then publicPolls} 
                <dl class="list-dl overflow-auto bg-surface-800 rounded-3xl p-1">
                    {#each publicPolls as poll}
                        <button class='w-[100%] text-left' on:click={() => {
                                modalComponent.props = {
                                    poll: poll
                                }
                                modalStore.trigger(modal)
                            }
                        }>
                            <div class="space-x-4 hover:bg-surface-500 cursor-pointer"> 
                                <span class="badge bg-primary-500">💀</span>
                                <span class="flex-auto">
                                    <dt>{poll.title}</dt>
                                    <dd>{poll.description}</dd>
                                </span>
                                <img src="./arrow-right-solid.svg" alt="arrow" class="w-5 h-5"/>
                            </div>
                        </button>
                    {/each}
                </dl>
            {/await}
        </div>
        <div class="flex flex-col w-2/6 p-10 gap-2">
            <h3>Private polls</h3>
            
            <label class="label">
                <span>Join by code</span>
                <div class="flex gap-1">
                    <input class="input" type="text" placeholder="xxxxxx" />
                    <button class="btn btn-primary hover:bg-surface-500">Join</button>
                </div>
            </label>
        </div>
    </div>
    <div class="flex flex-col w-1/4 bg-surface-900 rounded-3xl">
        <div class="flex flex-col p-10 gap-2">
            <h3>My Votes</h3>
        </div>
    </div>
</div>