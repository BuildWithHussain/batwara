<template>
	<Dialog
		v-model="showDialog"
		:options="{
			title: 'Settle expense',
		}"
	>
		<template #body-content>
			<div class="space-y-3">
				<FormControl
					type="number"
					v-model="settlementDetails.amount"
					placeholder="0.0"
					label="Amount"
				/>
				<Autocomplete
					v-model="settlementDetails.paid_by"
					placeholder="Who is paying?"
					:options="friendAutocompleteOptions"
				/>
				<Autocomplete
					v-model="settlementDetails.paid_to"
					placeholder="To whom?"
					:options="friendAutocompleteOptions"
				/>
			</div>

			<div
				class="mt-3 text-lg"
				v-if="settlementDetails.paid_by && settlementDetails.payed_to"
			>
				<span class="font-bold">{{ settlementDetails.paid_by.label }}</span> is paying
				<span class="font-bold">{{ settlementDetails.paid_to.label }}</span>
			</div>

			<div class="mt-2">
				<ErrorMessage :message="ledgerEntryResource.insert.error" />
			</div>
		</template>

		<template #actions>
			<Button
				:loading="ledgerEntryResource.insert.loading"
				variant="solid"
				theme="green"
				@click="recordPayment"
				>Record Payment</Button
			>
		</template>
	</Dialog>
</template>

<script setup>
import { computed, reactive, inject } from 'vue'
import { Dialog, Autocomplete, FormControl, ErrorMessage, createListResource } from 'frappe-ui'

import { sessionUser } from '@/data/session'

const showDialog = defineModel()
const friends = inject('friends')

const settlementDetails = reactive({
	paid_to: '',
	paid_by: '',
	amount: 0.0,
})

const friendAutocompleteOptions = computed(() => {
	const options = friends.value.map((f) => ({
		label: f.full_name,
		value: f.friend,
		image: f.user_image,
	}))

	options.push({
		label: 'You',
		value: sessionUser(),
	})

	return options
})

const ledgerEntryResource = createListResource({
	doctype: 'Split Ledger Entry',
})

function recordPayment() {
	ledgerEntryResource.insert.submit(
		{
			amount: settlementDetails.amount,
			credit_user: settlementDetails.paid_to.value,
			debit_user: settlementDetails.paid_by.value,
			is_settlement: true,
		},
		{
			onSuccess() {
				showDialog.value = false
				summaryResource.reload()
			},
		}
	)
}
</script>
