<script>
	import '../app.pcss';
	import Header from '../components/Header.svelte';
	import Footer from '../components/Footer.svelte';
	import { AppShell } from '@skeletonlabs/skeleton';
</script>


<AppShell>
	<svelte:fragment slot="header"><Header /></svelte:fragment>
	<slot />
	<svelte:fragment slot="pageFooter"><Footer /></svelte:fragment>
</AppShell>
