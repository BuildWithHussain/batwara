<template>
	<Card title="Expenses">
		<ListView :columns="[
			{
				label: 'Description',
				key: 'description',
				width: 4
			},
			{
				label: 'Amount',
				key: 'amount'
			}
		]" :options="{
			selectable: false,
			showTooltip: false,
			resizeColumn: false,
			emptyState: {
				title: 'No expense yet.'
			}
		}" :rows="expenseRows" rowKey="name" />
	</Card>
</template>

<script setup>
import {computed} from "vue";
import {createListResource, Card, ListView } from "frappe-ui";
import {sessionUser} from "@/data/session";

const expenses = createListResource({
	doctype: "Expense",
	fields: ["description", "amount", "name"],
	filters: {
		paid_by: sessionUser()
	},
	auto: true
})

const expenseRows = computed(() => {
	if (expenses.list.data) {
		return expenses.list.data.map((expense) => {
			return {
				...expense,
				amount: `₹${expense.amount}`
			}
		})
	}
	return [];
})
</script>
