<script lang="ts">
    import { currentTab } from "../../stores/dashboard";
    import { getUserPolls } from "../../helper/polls";
    import { Toast, getModalStore } from '@skeletonlabs/skeleton';
    import type { ModalComponent, ModalSettings } from '@skeletonlabs/skeleton';
    import EditPoll from "./EditPoll.svelte";
	import { polls } from "../../stores/polls";
			
    const modalStore = getModalStore();
    const modalComponent: ModalComponent = { ref: EditPoll };
    const modal: ModalSettings = {
        type: 'component',
        component: modalComponent,
    };

    $polls = getUserPolls();
</script>

<Toast />

<div class="flex justify-center max-h-[65vh] my-10">    
    {#if $currentTab === 2}
        {#await $polls}
            <div class="placeholder animate-pulse" />
        {:then currentPolls} 
            <dl class="list-dl overflow-auto w-3/4 bg-surface-800 rounded-3xl p-1">
                {#if currentPolls.length === 0}
                    <div class="p-2">
                        <h2>No polls found.</h2>
                    </div>
                {/if}
                {#each currentPolls as poll}
                
                    <div class="space-x-4">
                        <button class='p-2 hover:bg-surface-500 rounded-3xl'>
                            <img src="./share-from-square-regular.svg" alt="arrow" class="w-5 h-5"/>
                        </button>
                        <button class='w-[100%] text-left' on:click={() => {
                            modalComponent.props = {
                                poll: poll,
                                canEdit: false
                                }
                                modalStore.trigger(modal)
                            }
                        }>
                        <div class='hover:bg-surface-500 cursor-pointer'>
                            <span class="flex-auto">
                                <dt>{poll.title}</dt>                            
                            </span>
                            <img src="./arrow-right-solid.svg" alt="arrow" class="w-5 h-5"/>
                        </div>
                    </button>
                    </div>
                
                {/each}
                <button class="btn btn-primary variant-soft-surface w-[100%]" on:click={() => {
                        modalComponent.props = {
                            poll: {},
                            canEdit: true
                        }
                        modalStore.trigger(modal)
                    }
                }>
                    <img src="./plus-solid.svg" alt="plus" class="w-5 h-5"/>
                </button>
            </dl>
        {/await}
    {/if}
</div>