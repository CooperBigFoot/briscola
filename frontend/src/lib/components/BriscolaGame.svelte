<script>
	import GameHeader from './GameHeader.svelte';
	import GameArea from './GameArea.svelte';
	import PlayerHand from './PlayerHand.svelte';
	import GameFooter from './GameFooter.svelte';

	// Dummy data for demonstration
	const players = ['You', 'Opponent'];
	const hand = ['1_of_denari', '1_of_spade', '1_of_coppe'];
	const trumpCard = '1_of_bastoni';
</script>

<div class="flex flex-col h-screen bg-white text-gray-900 font-sans">
	<GameHeader />
	<GameArea {players} {trumpCard} />
	<PlayerHand {hand} />
	<GameFooter {players} />
</div>
