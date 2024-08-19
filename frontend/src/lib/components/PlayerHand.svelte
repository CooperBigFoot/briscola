<script>
	import Card from './Card.svelte';

	export let hand;
	export let isYourTurn;
</script>

<div class="flex justify-center items-center p-4 bg-gray-100">
	<div
		class="flex flex-row justify-center items-center space-x-2 sm:space-x-4 overflow-x-auto max-w-full"
	>
		{#each hand as card}
			<Card {card} size="large" isClickable={isYourTurn} isDraggable={isYourTurn} />
		{/each}
	</div>
</div>
