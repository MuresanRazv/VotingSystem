<script lang="ts">
    import { currentTab } from "../../stores/dashboard";
    import { getUserPolls } from "../../helper/polls";
    import { Toast, getModalStore } from '@skeletonlabs/skeleton';
    import type { ModalComponent, ModalSettings } from '@skeletonlabs/skeleton';
    import EditPoll from "./EditPoll.svelte";
	import { polls } from "../../stores/polls";
	import Share from "./Share.svelte";
    import isMobileStore from "../../stores/generalStore";
			
    let isMobile = false;

    isMobileStore.subscribe(value => {
        isMobile = value;
    });

    const modalStore = getModalStore();
    const modalPollComponent: ModalComponent = { ref: EditPoll };
    const pollModal: ModalSettings = {
        type: 'component',
        component: modalPollComponent,
    };
    const modalShareComponent: ModalComponent = { ref: Share };
    const shareModal: ModalSettings = {
        type: 'component',
        component: modalShareComponent,
    };

    $polls = getUserPolls();
</script>

<Toast />

<div class="flex justify-center max-h-[65vh] my-10">    
    {#if $currentTab === 2}
        {#await $polls}
            <div class="placeholder animate-pulse" />
        {:then currentPolls} 
            <dl class="list-dl overflow-auto {!isMobile ? 'w-3/4': 'w-[90%]'} bg-surface-800 rounded-3xl p-1">
                {#if currentPolls.length === 0}
                    <div class="p-2">
                        <h2>No polls found.</h2>
                    </div>
                {/if}
                {#each currentPolls as poll}
                    <div class="space-x-4">
                        <button class='p-2 hover:bg-surface-500 rounded-3xl' on:click={() => {
                            modalShareComponent.props = {
                                poll_code: poll.private_code,
                                poll_id: poll._id
                            };
                            modalStore.trigger(shareModal);
                        }}>
                            <img src="./share-from-square-regular.svg" alt="arrow" class="w-5 h-5"/>
                        </button>
                        <button class='variant-ghost-surface overflow-hidden max-h-20 btn whitespace-normal w-[100%] text-left' on:click={() => {
                                modalPollComponent.props = {
                                    poll: poll,
                                    canEdit: false
                                    };
                                    modalStore.trigger(pollModal);
                                }
                        }>
                        <div class='cursor-pointer'>
                            <span class='flex-auto {isMobile ? 'text-sm': ''}'>
                                <dt>{poll.title}</dt>                            
                            </span>
                            <img src="./arrow-right-solid.svg" alt="arrow" class="w-5 h-5"/>
                        </div>
                        </button>
                    </div>
                {/each}
                <button class="btn btn-primary variant-soft-surface w-[100%]" on:click={() => {
                        modalPollComponent.props = {
                            poll: {},
                            canEdit: true
                        }
                        modalStore.trigger(pollModal)
                    }
                }>
                    <img src="./plus-solid.svg" alt="plus" class="w-5 h-5"/>
                </button>
            </dl>
        {/await}
    {/if}
</div>