<script>
	import { User } from 'lucide-svelte';

	export let players;
</script>

<footer class="p-4 bg-gray-50 flex justify-between items-center border-t border-gray-200">
	<div class="flex items-center space-x-2">
		<div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center">
			<User size={20} class="text-gray-600" />
		</div>
		<span class="text-gray-600">{players[0]}</span>
	</div>
	<div class="text-gray-600">Score: 0</div>
</footer>
