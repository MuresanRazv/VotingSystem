<script>
    import { currentTab } from "../stores/dashboard";
    import { getUserPolls } from "../helper/polls";
</script>

<div class="flex justify-center overflow-auto max-h-[65vh] my-10">
    {#if $currentTab === 2}
        {#await getUserPolls()}
            <p>Loading...</p>
        {:then polls} 
            <dl class="list-dl w-3/4">
                {#each polls as poll}
                    <div class="space-x-4 hover:bg-surface-500 cursor-pointer">
                        <span class="badge bg-primary-500">💀</span>
                        <span class="flex-auto">
                            <dt>{poll.title}</dt>
                            <dd>{poll.description}</dd>
                        </span>
                        <p>hehe</p>
                    </div>
                {/each}       
            </dl> 
        {/await}
    {/if}
</div>