<script>
	export let card;
</script>

<div
	class="w-24 h-36 bg-white rounded-lg shadow-md flex items-center justify-center border border-gray-200 hover:border-blue-500 transition-colors duration-300 cursor-pointer"
>
	<img src={`/cards/${card}.png`} alt={card} class="w-full h-full object-cover rounded-lg" />
</div>
