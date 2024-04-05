<script>
    import { AppBar } from "@skeletonlabs/skeleton";
</script>

<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
	<svelte:fragment slot="lead"><img style="width: 35px; heigth: 35px;" src="./privacy-document-icon.svg" alt="img"/></svelte:fragment>
	This is a footer.
	<svelte:fragment slot="trail">Github account maybe?</svelte:fragment>
</AppBar>
