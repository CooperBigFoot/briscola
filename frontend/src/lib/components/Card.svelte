<script>
	export let card;
	export let size = 'normal';
	export let isClickable = true;
	export let isDraggable = false;

	function handleDragStart(event) {
		if (isDraggable) {
			event.dataTransfer.setData('application/json', JSON.stringify(card));
			event.dataTransfer.effectAllowed = 'move';
		}
	}
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
	draggable={isDraggable}
	on:dragstart={handleDragStart}
	class="relative bg-white rounded-lg {isClickable || isDraggable
		? 'shadow-lg hover:border-blue-500 hover:shadow-xl cursor-pointer'
		: ''} flex items-center justify-center border border-gray-200 transition-all duration-300 {size ===
	'large'
		? 'w-28 h-42 sm:w-32 sm:h-48 md:w-36 md:h-54 lg:w-40 lg:h-60'
		: size === 'small'
			? 'w-16 h-24 sm:w-20 sm:h-30 md:w-24 md:h-36 lg:w-28 lg:h-42'
			: 'w-24 h-36 sm:w-28 sm:h-42 md:w-32 md:h-48 lg:w-36 lg:h-54'}"
>
	<img src={`/cards/${card}.png`} alt={card} class="w-full h-full object-cover rounded-lg" />
</div>
