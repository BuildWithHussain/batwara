<template>
	<PageHeader heading="New Expense">
		<template #actions>
			<Button :loading="expenseListResource.insert.loading" @click="saveExpense"
				>Save</Button
			>
		</template>
	</PageHeader>

	<div class="space-y-3">
		<div>
			<ErrorMessage :message="expenseListResource.insert.error" />
		</div>

		<FormControl
			v-model="expenseDetails.description"
			label="Description"
			type="text"
			placeholder="Pizza from Zomato"
		/>
		<!-- TODO: later handle currency -->
		<FormControl
			v-model.number="expenseDetails.amount"
			label="Amount"
			type="number"
			placeholder="0.00"
		/>

		<FormControl v-model="expenseDetails.date" label="Expense Date" type="date" />

		<div class="pt-4 text-gray-800 font-semibold text-lg">
			Paid by <Button variant="outline">You</Button> and split
			<Dropdown
				:options="[
					{
						label: 'Equally',
						onClick: () => {
							expenseDetails.split_method = 'Equally'
						},
					},
					{
						label: 'Manually',
						onClick: () => {
							expenseDetails.split_method = 'Manually'
						},
					},
				]"
				:button="{
					label: expenseDetails.split_method,
					variant: 'outline',
				}"
			/>
		</div>

		<div>
			<h3 class="mb-2">Split with:</h3>

			<Autocomplete
				placeholder="Select friends"
				:options="friendAutocompleteOptions"
				v-model="expenseDetails.selected_friends"
				:multiple="true"
			/>
		</div>

		<div v-if="expenseDetails.split_method === 'Manually'">
			<ol class="space-y-3">
				<li v-for="friend in expenseDetails.selected_friends">
					<FormControl
						v-model.number="friend.amount"
						type="number"
						:label="friend.label"
						placeholder="0.0"
					/>
				</li>
			</ol>
		</div>
	</div>

	<div>
		<h3 class="font-semibold text-base my-4">Attach Receipts</h3>

		<FileUploader :fileTypes="['image/*']" @success="onFileUploadSuccess">
			<template
				v-slot="{
					file,
					uploading,
					progress,
					uploaded,
					message,
					error,
					total,
					success,
					openFileSelector,
				}"
			>
				<Button @click="openFileSelector" :loading="uploading">
					{{ uploading ? `Uploading ${progress}%` : 'Upload Image' }}
				</Button>
			</template>
		</FileUploader>

		<div class="mt-4">
			<ul class="grid grid-cols-4 gap-3 justify-center items-center">
				<li :key="attachment.name" v-for="attachment in attachments">
					<div class="w-20 h-20 border-gray-500 border rounded-sm overflow-hidden">
						<img class="object-contain" :src="attachment.file_url" />
					</div>
				</li>
			</ul>
		</div>
	</div>
</template>

<script setup>
import { inject, computed, reactive, ref } from 'vue'
import {
	FileUploader,
	FormControl,
	Dropdown,
	Autocomplete,
	createListResource,
	createResource,
	ErrorMessage,
} from 'frappe-ui'
import dayjs from 'dayjs'

import { useRouter } from 'vue-router'

const router = useRouter()

import PageHeader from '../components/common/PageHeader.vue'
import { sessionUser } from '@/data/session'

const friends = inject('friends')

const today = dayjs().format('YYYY-MM-DD')
const expenseDetails = reactive({
	description: '',
	amount: 0.0,
	currency: 'INR',
	split_method: 'Equally',
	date: today,
	selected_friends: [
		{
			label: 'You',
			value: sessionUser(),
		},
	],
})
const attachments = ref([])

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

// LOT OF NOISE, SO MUTED!

const expenseListResource = createListResource({
	doctype: 'Expense',
})

const linkAttachmentsResource = createResource({
	url: 'batwara.api.link_attachments_to_expense',
	onSuccess() {
		router.replace({ name: 'Dashboard' })
	},
})

function saveExpense() {
	expenseListResource.insert.submit(
		{
			...expenseDetails,
			paid_by: sessionUser(),
			splits: expenseDetails.selected_friends.map((f) => ({
				user: f.value,
				amount: f.amount || 0.0,
			})),
		},
		{
			onSuccess(data) {
				// link attachments
				linkAttachmentsResource.submit({
					attachments: attachments.value,
					name: data.name,
				})
			},
		}
	)
}

function onFileUploadSuccess(fileDoc) {
	attachments.value.push(fileDoc)
}
</script>
