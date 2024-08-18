<script>
	import { User } from 'lucide-svelte';
	import Card from './Card.svelte';

	export let players;
	export let trumpCard;
</script>

<main class="flex-grow flex flex-col justify-between p-8">
	<!-- Opponent -->
	<div class="flex justify-center mb-12">
		<div class="text-center">
			<div class="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center mb-2">
				<User size={24} class="text-gray-600" />
			</div>
			<p class="text-sm text-gray-600">{players[1]}</p>
		</div>
	</div>

	<!-- Center Area -->
	<div class="flex justify-center items-center space-x-12">
		<!-- Trump Card -->
		<div class="text-center">
			<Card card={trumpCard} />
			<p class="mt-2 text-sm text-gray-600">Trump</p>
		</div>

		<!-- Play Area -->
		<div class="w-72 h-72 border-2 border-gray-200 rounded-full flex items-center justify-center">
			<p class="text-xl text-gray-400">Play Area</p>
		</div>

		<!-- Deck -->
		<div class="text-center">
			<div class="w-24 h-36 bg-gray-100 rounded-lg shadow-md"></div>
			<p class="mt-2 text-sm text-gray-600">Deck</p>
		</div>
	</div>
</main>
