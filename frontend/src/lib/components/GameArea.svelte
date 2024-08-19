<script>
	import { User } from 'lucide-svelte';
	import Card from './Card.svelte';
	import { createEventDispatcher } from 'svelte';

	export let players;
	export let trumpCard;
	export let cardsInDeck;
	export let isYourTurn;

	let playedCard = null;
	const dispatch = createEventDispatcher();

	function handleDragOver(event) {
		event.preventDefault();
		event.dataTransfer.dropEffect = 'move';
	}

	function handleDrop(event) {
		event.preventDefault();
		if (!isYourTurn) return;
		const cardData = event.dataTransfer.getData('application/json');
		if (cardData) {
			playedCard = JSON.parse(cardData);
			dispatch('cardPlayed', playedCard);
		}
	}
</script>

<main class="h-full flex flex-col justify-between p-4">
	<!-- Opponent Icon -->
	<div class="flex justify-center mb-4">
		<div class="text-center">
			<div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center mb-1">
				<User size={20} class="text-gray-600" />
			</div>
			<p class="text-xs text-gray-600">{players[1]}</p>
		</div>
	</div>

	<!-- Play Area with Trump and Deck Info -->
	<div class="flex-grow flex items-center justify-center">
		<div class="w-full max-w-2xl mx-auto">
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<div
				class="border-2 border-gray-200 rounded-3xl flex flex-col {isYourTurn
					? 'bg-green-50 shadow-lg'
					: ''}"
				on:dragover={handleDragOver}
				on:drop={handleDrop}
			>
				<!-- Turn Indicator -->
				<p class="text-base text-gray-600 mt-4 mb-2 font-semibold text-center">
					{#if isYourTurn}
						Your turn, drag & drop
					{:else}
						Opponent's turn
					{/if}
				</p>

				<!-- Play Area -->
				<div
					class="flex-grow flex items-center justify-center p-4 sm:p-5 md:p-6 min-h-[150px] h-[20vh] sm:h-[25vh] md:h-[30vh] lg:h-[35vh]"
				>
					<div class="w-full h-full flex items-center justify-center">
						{#if playedCard}
							<Card card={playedCard} isClickable={false} size="large" />
						{:else}
							<div class="text-gray-400 text-lg">Drop a card here</div>
						{/if}
					</div>
				</div>

				<!-- Bottom Row with Trump and Deck Cards -->
				<div class="flex justify-between items-end p-4">
					<!-- Trump Card -->
					<div class="text-center">
						<Card card={trumpCard} isClickable={false} size="small" />
						<p class="mt-1 text-xs text-gray-600">Trump</p>
					</div>

					<!-- Deck Info -->
					<div class="flex flex-col items-center">
						<div class="relative">
							<Card card="retro" isClickable={false} size="small" />
							<div
								class="absolute inset-0 bg-gray-900 bg-opacity-70 flex items-center justify-center rounded-lg"
							>
								<span class="text-white font-bold text-lg">{cardsInDeck}</span>
							</div>
						</div>
						<p class="mt-1 text-xs text-gray-600">Cards in deck</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</main>
