<script>
	import GameHeader from './GameHeader.svelte';
	import GameArea from './GameArea.svelte';
	import PlayerHand from './PlayerHand.svelte';
	import GameFooter from './GameFooter.svelte';
	import { onMount } from 'svelte';

	// Dummy data for demonstration
	const players = ['You', 'Opponent'];
	const hand = ['1_of_denari', '1_of_spade', '1_of_coppe'];
	const trumpCard = '1_of_bastoni';
	const cardsInDeck = 37; // Example value

	let isMobile = false;

	onMount(() => {
		const mediaQuery = window.matchMedia('(max-width: 640px)');
		isMobile = mediaQuery.matches;
		mediaQuery.addEventListener('change', handleMediaQueryChange);

		return () => {
			mediaQuery.removeEventListener('change', handleMediaQueryChange);
		};
	});

	function handleMediaQueryChange(e) {
		isMobile = e.matches;
	}
</script>

<div class="flex flex-col h-screen bg-white text-gray-900 font-sans">
	<GameHeader />
	<GameArea {players} {trumpCard} {cardsInDeck} />
	<div class={isMobile ? 'mt-auto' : 'flex-grow'}>
		<PlayerHand {hand} />
	</div>
	<GameFooter {players} />
</div>
