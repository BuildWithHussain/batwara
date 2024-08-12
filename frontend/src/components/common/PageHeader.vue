<template>
	<div class="mb-4 flex justify-between">
		<h2 class="font-bold text-gray-900 text-2xl">{{ props.heading }}</h2>
		<slot name="actions"></slot>
	</div>
</template>

<script setup>
const props = defineProps({
	heading: String,
})
</script>
