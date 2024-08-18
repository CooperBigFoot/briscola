<script>
	import Card from './Card.svelte';
	import { onMount } from 'svelte';

	export let hand;

	let containerWidth;
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

	$: cardWidth = 96; // 24rem (w-24) converted to pixels
	$: cardHeight = 144; // 36rem (h-36) converted to pixels
	$: fanSpread = isMobile ? Math.min(containerWidth / hand.length, cardWidth) : cardWidth;
	$: fanRotation = isMobile ? 5 : 0; // Degree of rotation for each card in the fan
</script>

<div class="relative" bind:clientWidth={containerWidth}>
	<div class="flex justify-center mt-12 {isMobile ? 'h-48' : ''}">
		{#each hand as card, index (card)}
			<div
				class="absolute transition-all duration-300 ease-in-out"
				style="
					left: calc(50% + {(index - (hand.length - 1) / 2) * fanSpread}px);
					transform: translateX(-50%) {isMobile
					? `rotate(${(index - (hand.length - 1) / 2) * fanRotation}deg)`
					: ''};
					z-index: {index};
				"
			>
				<Card {card} />
			</div>
		{/each}
	</div>
</div>

<style>
	/* Add any additional styles here if needed */
</style>
