<template>
	<Card title="Summary">
		<div v-if="summaryResource.loading">
			<LoadingText />
		</div>
		<div v-else-if="summaryResource.data">
			<ul class="flex flex-col space-y-3">
				<li :key="friend" v-for="details, friend in summaryResource.data">
					<div class="flex items-center justify-between">
						<div class="flex items-center space-x-2">
							<Avatar size="xl" :image="details.user_image" :label="details.full_name" />

							<div v-if="details.type === 'to_send'">
								You owe {{ details.full_name }} ₹{{ details.net_amount }}.
							</div>

							<div v-else-if="details.type === 'to_receive'">
								{{ details.full_name }} owes you ₹{{ details.net_amount }}.
							</div>
						</div>

						<Button size="lg" icon="file-text" />
					</div>
				</li>
			</ul>
		</div>

		<template #actions>
			<Button @click="showSettleUpDialog = true" variant="outline" theme="green">Settle Up</Button>
		</template>
	</Card>

	<ErrorMessage :message="summaryResource.error" />

	<SettlementDialog v-model="showSettleUpDialog" />
</template>

<script setup>
import { ref } from "vue";
import {createResource, LoadingText, Card, Avatar} from "frappe-ui";
import SettlementDialog from "../dashboard/SettlementDialog.vue";

const showSettleUpDialog = ref(false);

const summaryResource = createResource({
	url: "batwara.api.get_summary_for_session_user",
	auto: true,
	onSuccess(d) {
		console.log(d)
	}
})
</script>
