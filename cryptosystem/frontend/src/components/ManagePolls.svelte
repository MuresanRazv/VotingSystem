<script lang="ts">
    import { currentTab } from "../stores/dashboard";
    import { getUserPolls } from "../helper/polls";
    import { getModalStore } from '@skeletonlabs/skeleton';
    import type { ModalComponent, ModalSettings } from '@skeletonlabs/skeleton';
    import EditPoll from "./EditPoll.svelte";
			
    const modalStore = getModalStore();
    const modalComponent: ModalComponent = { ref: EditPoll };
    const modal: ModalSettings = {
	type: 'component',
    component: modalComponent,
};

</script>

<div class="flex justify-center overflow-auto max-h-[65vh] my-10">
    {#if $currentTab === 2}
        {#await getUserPolls()}
            <p>Loading...</p>
        {:then polls} 
            <dl class="list-dl w-3/4">
                {#each polls as poll}
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
    {/if}
</div>