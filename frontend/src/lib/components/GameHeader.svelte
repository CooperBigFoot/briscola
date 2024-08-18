<script>
	import { Settings } from 'lucide-svelte';
</script>

<header class="p-4 flex justify-between items-center border-b border-gray-200">
	<div class="flex items-center space-x-2">
		<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path
				d="M3 3H21V21H3V3Z"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
			<path
				d="M7 7H17V17H7V7Z"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			/>
		</svg>
		<h1 class="text-lg font-bold">Briscola 1v1</h1>
	</div>
	<nav class="flex space-x-4">
		<a href="#" class="text-sm text-gray-600 hover:text-blue-500">Rules</a>
		<a href="#" class="text-sm text-gray-600 hover:text-blue-500">Stats</a>
	</nav>
	<button class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-300">
		<Settings size={18} />
	</button>
</header>
