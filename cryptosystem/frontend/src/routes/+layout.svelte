<script>
	import '../app.pcss';
	import Header from '../components/base/Header.svelte';
	import Footer from '../components/base/Footer.svelte';
	import { AppShell, Drawer } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	import isMobileStore from '../stores/generalStore';
	import { onMount } from 'svelte';
	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

	onMount(() => {
		isMobileStore.set(window.innerWidth < 768);
		window.addEventListener('resize', () => {
			isMobileStore.set(window.innerWidth < 768);
		});
	});
</script>

<AppShell>
	<svelte:fragment slot="header"><Header /></svelte:fragment>
	<slot />
	<svelte:fragment slot="pageFooter"><Footer /></svelte:fragment>
</AppShell>
