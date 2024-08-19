<script>
	import GameHeader from './GameHeader.svelte';
	import GameArea from './GameArea.svelte';
	import PlayerHand from './PlayerHand.svelte';
	import { onMount } from 'svelte';

	// Dummy data for demonstration
	const players = ['You', 'Opponent'];
	let hand = ['re_of_denari', 're_of_spade', 're_of_coppe'];
	const trumpCard = '3_of_bastoni';
	const cardsInDeck = 37; // Example value

	let isYourTurn = true;

	function onCardPlayed(event) {
		const playedCard = event.detail;
		hand = hand.filter((card) => card !== playedCard);
		isYourTurn = false; // Toggle turn after playing a card
	}
</script>

<div class="flex flex-col h-screen bg-white text-gray-900 font-sans">
	<GameHeader />
	<div class="flex-grow flex flex-col">
		<div class="flex-grow">
			<GameArea {players} {trumpCard} {cardsInDeck} {isYourTurn} on:cardPlayed={onCardPlayed} />
		</div>
		<div class="mt-auto">
			<PlayerHand {hand} {isYourTurn} />
		</div>
	</div>
</div>
