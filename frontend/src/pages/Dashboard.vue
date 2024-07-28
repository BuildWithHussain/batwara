<template>
	<div>
		<FriendsList />

		<div class="mt-5">
			<Button route="/new-expense" variant="solid" theme="green">+ Add Expense</Button>
		</div>

		<div class="mt-5">
			<PageHeader heading="Summary" />
		</div>

		<div v-if="summaryResource.loading">
			<LoadingText />
		</div>
		<div v-else-if="summaryResource.data">
			<ul>
				<li :key="friend" v-for="details, friend in summaryResource.data">
					<div v-if="details.type === 'to_send'">
						You owe {{ details.full_name }} ₹{{ details.net_amount }}.
					</div>

					<div v-else-if="details.type === 'to_receive'">
						{{ details.full_name }} ows you ₹{{ details.net_amount }}.
					</div>
				</li>
			</ul>
		</div>

		<div class="mt-5">
			<Button @click="showSettleUpDialog = true" variant="outline" theme="green">Settle Up</Button>
		</div>
	</div>

	<Dialog v-model="showSettleUpDialog" :options="{
		'title': 'Settle expense'
	}">
		<template #body-content>
			<div class="space-y-3">
				<FormControl type="number" v-model="settlementDetails.amount" placeholder="0.0" label="Amount" />
				<Autocomplete v-model="settlementDetails.paid_by" placeholder="Who is paying?" :options="friendAutocompleteOptions" />
				<Autocomplete v-model="settlementDetails.paid_to" placeholder="To whom?" :options="friendAutocompleteOptions" />
			</div>

			<div class="mt-3 text-lg" v-if="settlementDetails.paid_by && settlementDetails.payed_to">
				<span class="font-bold">{{ settlementDetails.paid_by.label }}</span> is paying <span class="font-bold">{{ settlementDetails.paid_to.label }}</span>
			</div>

			<div class="mt-2">
				<ErrorMessage :message="ledgerEntryResource.insert.error" />
			</div>
  		</template>

		<template #actions>
			<Button :loading="ledgerEntryResource.insert.loading" variant="solid" theme="green" @click="recordPayment">Record Payment</Button>
		</template>
	</Dialog>
</template>

<script setup>
import { inject, ref, computed, reactive } from "vue";
import { createResource, createListResource, LoadingText, Dialog, Autocomplete, FormControl, ErrorMessage } from "frappe-ui";
import { sessionUser } from "@/data/session";
import PageHeader from "../components/common/PageHeader.vue";
import FriendsList from "../components/friends/List.vue";

const friends = inject("friends");

const settlementDetails = reactive({
	"paid_to": "",
	"paid_by": "",
	"amount": 0.0
})

const showSettleUpDialog = ref(false);

const summaryResource = createResource({
	url: "batwara.api.get_summary_for_session_user",
	auto: true,
	onSuccess(d) {
		console.log(d)
	}
})

const friendAutocompleteOptions = computed(() => {
	const options = friends.value.map(f => ({label: f.full_name, value: f.friend, image: f.user_image}))

	options.push({
		label: 'You',
		value: sessionUser(),
	})

	return options;
})

const ledgerEntryResource = createListResource({
	doctype: "Split Ledger Entry"
})

function recordPayment() {
	ledgerEntryResource.insert.submit({
		"amount": settlementDetails.amount,
		"credit_user": settlementDetails.paid_to.value,
		"debit_user": settlementDetails.paid_by.value,
		"is_settlement": true
	}, {
		onSuccess() {
			showSettleUpDialog.value = false;
			summaryResource.reload();
		}
	})
}
</script>
