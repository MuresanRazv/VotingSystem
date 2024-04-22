<script lang="ts">
	import { Toast, getModalStore, getToastStore } from "@skeletonlabs/skeleton";
    import type { ModalComponent, ModalSettings, ToastSettings } from '@skeletonlabs/skeleton';
	import { getPublicPolls, getPrivatePoll } from "../../helper/polls";
    import { polls } from "../../stores/polls";
    import VotePoll from "./VotePoll.svelte";
	import { getUserVotes } from "../../helper/votes";
	import { votes } from "../../stores/votes";
    import user from "../../stores/user";
    import PollStatus from "./PollStatus.svelte";
	import { onMount } from "svelte";
    
    const modalStore = getModalStore();
    const modalComponent: ModalComponent = { ref: VotePoll };
    const statusModalComponent: ModalComponent = { ref: PollStatus };
    const pollModal: ModalSettings = {
        type: 'component',
        component: modalComponent,
    };
    const pollStatusModal: ModalSettings = {
        type: 'component',
        component: statusModalComponent,
    };

    $polls = getPublicPolls();
    $votes = getUserVotes($user._id);

    let privateCode = '';
    const toastStore = getToastStore();
    const t: ToastSettings = {
	    message: 'Invalid code! Please enter a valid code.',
    };
    function handleJoin() {
        if (privateCode.length === 6) {
            getPrivatePoll(privateCode)
            .then((response: any) => {
                if (response.detail) {
                    throw response.detail;
                }
                modalComponent.props = {
                    poll: response
                };
                modalStore.trigger(pollModal);
            })
            .catch(() => {
                toastStore.trigger(t);
            });
        } else {
            toastStore.trigger(t);
        }
    }

    onMount(() => {
        const urlParams = new URLSearchParams(window.location.search);

        if (urlParams.has("poll_code")) {
            let poll_code = urlParams.get("poll_code");
            if (poll_code?.length === 6) {
                getPrivatePoll(poll_code)
                .then((response: any) => {
                    if (response.created_by === $user._id) {
                        toastStore.trigger({
                            message: 'You cannot vote on your own poll',
                        });
                    } else if (response.id && response.message) {
                        // user voted already, let status component handle it
                        statusModalComponent.props = {
                            poll_id: response.id
                        };
                        modalStore.trigger(pollStatusModal);
                    } else {
                        // user can vote
                        modalComponent.props = {
                            poll: response
                        };
                        modalStore.trigger(pollModal);
                    }
                })
                .finally(() => {
                    urlParams.delete("poll_code");
                    window.history.replaceState({}, document.title, window.location.pathname);
                });
            } else {
                toastStore.trigger(t);
            }
        }
    })
</script>

<Toast />

<div class="flex flex-col overflow-auto max-h-[65vh] m-10 gap-2">
    <div class="flex flex-row w-[100%] gap-5">
        <div class="flex flex-col w-4/6 p-10 gap-5 bg-surface-900 rounded-3xl">
            <h3>Public polls</h3>
            {#await $polls}
                <div class="placeholder animate-pulse" />
            {:then publicPolls} 
                <dl class="list-dl overflow-auto bg-surface-800 rounded-3xl p-1">
                    {#if publicPolls.length === 0}
                        <p class="p-5">No public polls available</p>
                    {:else}
                        {#each publicPolls as poll}
                            <button class='w-[100%] text-left' on:click={() => {
                                    modalComponent.props = {
                                        poll: poll
                                    }
                                    modalStore.trigger(pollModal)
                                }
                            }>
                                <div class="space-x-4 hover:bg-surface-500 cursor-pointer">
                                    <span class="flex-auto">
                                        <dt>{poll.title}</dt>                                        
                                    </span>
                                    <img src="./arrow-right-solid.svg" alt="arrow" class="w-5 h-5"/>
                                </div>
                            </button>
                        {/each}
                    {/if}
                </dl>
            {/await}
        </div>
        <div class="flex flex-col w-2/6 p-10 gap-2 bg-surface-900 rounded-3xl">
            <h3>Private polls</h3>
            
            <label class="label">
                <span>Join by code</span>
                <div class="flex gap-1">
                    <input class="input" type="text" placeholder="xxxxxx" bind:value={privateCode} />
                    <button class="btn btn-primary hover:bg-surface-500" on:click={handleJoin}>Join</button>
                </div>
            </label>
        </div>
    </div>
    <div class="flex flex-col w-[100%] bg-surface-900 rounded-3xl">
        <div class="flex flex-col p-10 gap-2">
            <h3>Voted Polls</h3>
            {#await $votes}
                <div class="placeholder animate-pulse" />
            {:then userVotes} 
                <dl class="list-dl overflow-auto bg-surface-800 rounded-3xl p-1">
                    {#if userVotes.length === 0}
                        <p class="p-5">No voted polls available</p>
                    {/if}
                    {#each userVotes as vote}
                        <button class='w-[100%] text-left'  on:click={() => {
                            statusModalComponent.props = {
                                poll_id: vote.poll._id
                            }
                            modalStore.trigger(pollStatusModal)
                        }}>
                            <div class="space-x-4 hover:bg-surface-500 cursor-pointer">
                                <span class="flex-auto">
                                    <dt>{vote.poll.title}</dt>                                    
                                </span>
                                <img src="./arrow-right-solid.svg" alt="arrow" class="w-5 h-5"/>
                            </div>
                        </button>
                    {/each}
                </dl>
            {/await}
        </div>
    </div>
</div>