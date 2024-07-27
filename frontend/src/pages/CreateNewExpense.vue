<template>
	<PageHeader heading="New Expense">
		<template #actions>
			<Button :loading="expenseListResource.insert.loading" @click="saveExpense">Save</Button>
		</template>
	</PageHeader>

	<div class="space-y-3">
		<div>
			<ErrorMessage :message="expenseListResource.insert.error" />
		</div>

		<FormControl v-model="expenseDetails.description" label="Description" type="text" placeholder="Pizza from Zomato" />
		<!-- TODO: later handle currency -->
		<FormControl v-model.number="expenseDetails.amount" label="Amount" type="number" placeholder="0.00" />

		<FormControl v-model="expenseDetails.date" label="Expense Date" type="date" />

		<div class="pt-4 text-gray-800 font-semibold text-lg">
			Paid by <Button variant="outline">You</Button> and split
			<Dropdown
				:options="[
					{
						label: 'Equally',
						onClick: () => { expenseDetails.split_method = 'Equally' },
					},
					{
						label: 'Manually',
						onClick: () => { expenseDetails.split_method = 'Manually' },
					},
				]"
				:button="{
					label: expenseDetails.split_method,
					variant: 'outline'
				}" />
		</div>

		<div>
			<h3 class="mb-2">Split with:</h3>

			<Autocomplete placeholder="Select friends" :options="friendAutocompleteOptions" v-model="expenseDetails.selected_friends" :multiple="true" />
		</div>
	</div>
</template>

<script setup>
import { inject, computed, reactive } from "vue";
import { FormControl, Dropdown, Autocomplete, createListResource, ErrorMessage } from "frappe-ui";
import dayjs from "dayjs";

import { useRouter } from "vue-router";

const router = useRouter();


import PageHeader from "../components/common/PageHeader.vue";
import {sessionUser} from "@/data/session";

const friends = inject("friends");

const today = dayjs().format("YYYY-MM-DD")
const expenseDetails =  reactive({
	description: '',
	amount: 0.0,
	currency: 'INR',
	split_method: "Equally",
	date: today,
	selected_friends: [{
		label: 'You',
		value: sessionUser()
	}]
})

const friendAutocompleteOptions = computed(() => {
	const options = friends.value.map(f => ({label: f.full_name, value: f.friend, image: f.user_image}))

	options.push({
		label: 'You',
		value: sessionUser(),
	})

	return options;
})

const expenseListResource = createListResource({
	doctype: "Expense",
})

function saveExpense() {
	expenseListResource.insert.submit(
		{
			...expenseDetails,
			paid_by: sessionUser(),
			splits: expenseDetails.selected_friends.map((f) => ({
			user: f.value,
		}))
},
{
	onSuccess() {
		router.replace({name: "Dashboard"})
	}
}
)
}
</script>


