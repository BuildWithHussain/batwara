<template>
	<VOtpInput
		input-classes="w-10 h-10 font-bold m-1 rounded border-gray-400 focus:border-0 focus:ring-2 focus:ring-green-500"
		:should-auto-focus="true"
		:should-focus-order="true"
		v-model="model"
		separator="-"
		@on-change="(v) => model = v"
		@on-complete="(v) => emit('complete', v)"
		:placeholder="['*', '*', '*', '*', '*', '*']"
		:num-inputs="6"
		:is-disabled="props.disabled"
	/>
</template>

<script setup>
import VOtpInput from "vue3-otp-input";

const props = defineProps({
	disabled: Boolean
})

const model = defineModel()
const emit = defineEmits(['complete'])
</script>
