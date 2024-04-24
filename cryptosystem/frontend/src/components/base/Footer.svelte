<script>
    import { AppBar } from "@skeletonlabs/skeleton";
</script>

<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
	<svelte:fragment slot="lead">
		<img class="w-10 h-10" src="./privacy-document-icon.svg" alt="img"/>
	</svelte:fragment>
	<svelte:fragment slot="trail">
		<a href="https://github.com/MuresanRazv">
			<span class="badge-icon variant-ghost w-7 h-7">
				<img src="./github.svg" alt="img"/>
			</span>
		</a>
	</svelte:fragment>
</AppBar>
