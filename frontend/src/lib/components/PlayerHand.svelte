<script>
	import Card from './Card.svelte';
	import { onMount } from 'svelte';

	export let hand;

	let isMobile = false;

	onMount(() => {
		const mediaQuery = window.matchMedia('(max-width: 640px)');
		isMobile = mediaQuery.matches;
		mediaQuery.addListener(handleMediaQueryChange);

		return () => {
			mediaQuery.removeListener(handleMediaQueryChange);
		};
	});

	function handleMediaQueryChange(e) {
		isMobile = e.matches;
	}
</script>

<div class="relative">
	{#if isMobile}
		<div class="grid grid-cols-3 gap-2 p-2">
			{#each hand as card}
				<div class="w-full">
					<Card {card} />
				</div>
			{/each}
		</div>
	{:else}
		<div class="flex justify-center mt-4 sm:mt-8 md:mt-12 h-32 sm:h-40 md:h-48">
			{#each hand as card, index (card)}
				<div
					class="absolute transition-all duration-300 ease-in-out"
					style="
						left: calc(50% + {(index - (hand.length - 1) / 2) * 60}px);
						transform: translateX(-50%) rotate({(index - (hand.length - 1) / 2) * 5}deg);
						z-index: {index};
					"
				>
					<Card {card} />
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	/* Add any additional styles here if needed */
</style>
