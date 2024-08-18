<script>
	export let card;
	export let size = 'normal';
</script>

<div
	class="bg-white rounded-lg shadow-md flex items-center justify-center border border-gray-200 hover:border-blue-500 transition-colors duration-300 cursor-pointer {size ===
	'large'
		? 'w-24 h-36'
		: 'w-16 h-24'}"
>
	<img src={`/cards/${card}.png`} alt={card} class="w-full h-full object-cover rounded-lg" />
</div>
