<template>
	<div class="space-y-4">
		<BalanceSummary />
		<ExpenseList />
	</div>
</template>

<script setup>
import BalanceSummary from '../components/dashboard/BalanceSummary.vue'
import ExpenseList from '../components/dashboard/ExpenseList.vue'
</script>
