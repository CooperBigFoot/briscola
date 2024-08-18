<script>
	import Card from './Card.svelte';

	export let hand;
</script>

<div class="flex justify-center space-x-4 mt-12">
	{#each hand as card, index (index)}
		<Card {card} />
	{/each}
</div>
