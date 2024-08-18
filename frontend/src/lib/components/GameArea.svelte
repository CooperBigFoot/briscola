<script>
	import { User } from 'lucide-svelte';
	import Card from './Card.svelte';
	import { onMount } from 'svelte';

	export let players;
	export let trumpCard;

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

<main class="flex-grow flex flex-col justify-between p-4 sm:p-8">
	<!-- Opponent -->
	<div class="flex justify-center mb-6 sm:mb-12">
		<div class="text-center">
			<div
				class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gray-100 flex items-center justify-center mb-2"
			>
				<User size={20} class="text-gray-600" />
			</div>
			<p class="text-xs sm:text-sm text-gray-600">{players[1]}</p>
		</div>
	</div>

	<!-- Center Area -->
	<div class="flex justify-center items-center space-x-4 sm:space-x-12">
		<!-- Trump Card and Deck -->
		<div class="relative w-24 h-36">
			{#if isMobile}
				<div class="absolute top-0 left-0 z-20 w-24 h-36">
					<Card card="retro" />
				</div>
				<div
					class="absolute top-1/2 left-1/2 z-10 w-36 h-24 transform -translate-y-1/2 translate-x-1/4 rotate-180"
				>
					<Card card={trumpCard} />
				</div>
			{:else}
				<div class="text-center">
					<Card card={trumpCard} />
					<p class="mt-2 text-xs sm:text-sm text-gray-600">Trump</p>
				</div>
			{/if}
		</div>

		<!-- Play Area -->
		<div
			class="w-48 h-48 sm:w-72 sm:h-72 border-2 border-gray-200 rounded-full flex items-center justify-center"
		>
			<p class="text-base sm:text-xl text-gray-400">Play Area</p>
		</div>

		<!-- Deck (only visible on desktop) -->
		{#if !isMobile}
			<div class="text-center">
				<Card card="retro" />
				<p class="mt-2 text-xs sm:text-sm text-gray-600">Deck</p>
			</div>
		{/if}
	</div>
</main>
