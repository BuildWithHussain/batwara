<template>
	<Card title="Summary">
		<div v-if="summaryResource.loading">
			<LoadingText />
		</div>
		<div v-else-if="summaryResource.data">
			<ul class="flex flex-col space-y-3">
				<li :key="friend" v-for="(details, friend) in summaryResource.data">
					<div class="flex items-center justify-between">
						<div class="flex items-center space-x-2">
							<Avatar
								size="xl"
								:image="details.user_image"
								:label="details.full_name"
							/>
							<div v-if="details.type === 'to_send'">
								You owe
								<span class="font-semibold">{{ details.full_name }}</span> ₹{{
									details.net_amount
								}}
							</div>

							<div v-else-if="details.type === 'to_receive'">
								<span class="font-semibold">{{ details.full_name }}</span> owes you
								₹{{ details.net_amount }}
							</div>
						</div>

						<Button
							class="text-gray-700"
							@click="
								() => {
									selectedFriend.name = friend
									selectedFriend.full_name = details.full_name
									transactionHistoryResource.reload()
									showTransactionHistoryDialog = true
								}
							"
							size="lg"
							icon="file-text"
						/>
					</div>
				</li>
			</ul>
		</div>

		<template #actions>
			<Button @click="showSettleUpDialog = true" variant="outline" theme="green"
				>Settle Up</Button
			>
		</template>
	</Card>

	<ErrorMessage :message="summaryResource.error" />

	<SettlementDialog v-model="showSettleUpDialog" />

	<Dialog
		:options="{ title: `History with ${selectedFriend.full_name}` }"
		v-model="showTransactionHistoryDialog"
	>
		<template #body-content>
			<div>
				<ol class="space-y-3">
					<li
						class="text-gray-800 font-medium"
						v-for="item in transactionHistoryResource.data || []"
					>
						<div
							class="flex flex-row space-x-2 items-center"
							v-if="item.is_settlement"
						>
							<FeatherIcon class="w-5 text-green-700" name="dollar-sign" />
							<div>
								{{ getDisplayNameForHistory(item.debit_user) }} paid
								<span class="font-bold">₹{{ item.amount }}</span> to
								{{ getDisplayNameForHistory(item.credit_user) }}.
							</div>
						</div>
						<div class="flex flex-row space-x-2 items-center" v-else>
							<FeatherIcon class="w-5 text-amber-700" name="file" />
							<div>
								{{ getDisplayNameForHistory(item.credit_user) }} borrowed
								<span class="font-bold">₹{{ item.amount }}</span> from
								{{ getDisplayNameForHistory(item.debit_user) }}.
							</div>
						</div>
					</li>
				</ol>
			</div>
		</template>
	</Dialog>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { createResource, LoadingText, Card, Avatar, Dialog, FeatherIcon } from 'frappe-ui'
import SettlementDialog from '../dashboard/SettlementDialog.vue'
import { sessionUser } from '@/data/session'

const showSettleUpDialog = ref(false)
const showTransactionHistoryDialog = ref(false)

const summaryResource = createResource({
	url: 'batwara.api.get_summary_for_session_user',
	auto: true,
})

const selectedFriend = reactive({})
const transactionHistoryResource = createResource({
	url: 'batwara.api.get_transaction_history_with_friend',
	makeParams() {
		return {
			friend: selectedFriend.name,
		}
	},
})

function getDisplayNameForHistory(name) {
	if (name === sessionUser()) {
		return 'You'
	}

	if (name === selectedFriend.name) {
		return selectedFriend.full_name
	}

	return name
}
</script>
