<script>
	import { User } from 'lucide-svelte';
	import Card from './Card.svelte';
	import { onMount } from 'svelte';

	export let players;
	export let trumpCard;
	export let cardsInDeck;
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

<main class="flex-grow flex flex-col justify-between p-4">
	<!-- Trump and Deck Info -->
	<div class="flex justify-between items-start mb-8">
		<div class="text-center">
			<Card card={trumpCard} />
			<p class="mt-1 text-xs text-gray-600">Trump</p>
		</div>
		<div class="flex flex-col items-center">
			<div
				class="w-16 h-24 bg-white rounded-lg shadow-md flex items-center justify-center border border-gray-200 relative"
			>
				<div class="absolute inset-0 bg-red-800 rounded-lg"></div>
				<div class="absolute inset-0 border-4 border-white rounded-lg"></div>
				<span class="relative text-white font-bold">{cardsInDeck}</span>
			</div>
			<p class="mt-1 text-xs text-gray-600">Cards in deck</p>
		</div>
	</div>

	<!-- Opponent Icon -->
	<div class="flex justify-center mb-4">
		<div class="text-center">
			<div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center mb-1">
				<User size={20} class="text-gray-600" />
			</div>
			<p class="text-xs text-gray-600">{players[1]}</p>
		</div>
	</div>

	<!-- Play Area -->
	<div
		class="w-64 h-64 mx-auto border-2 border-gray-200 rounded-full flex items-center justify-center mb-8"
	>
		<p class="text-lg text-gray-400">Play Area</p>
	</div>

	<!-- Player's Hand -->
	<div class="flex justify-center space-x-4 mb-4">
		{#if hand && hand.length > 0}
			{#each hand as card}
				<Card {card} size="large" />
			{/each}
		{/if}
	</div>
</main>
