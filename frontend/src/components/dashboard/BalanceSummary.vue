<template>
	<PageHeader heading="Summary" />
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
					{{ details.full_name }} owes you ₹{{ details.net_amount }}.
				</div>
			</li>
		</ul>
	</div>

	<ErrorMessage :message="summaryResource.error" />
</template>

<script setup>
import {createResource, LoadingText} from "frappe-ui";
import PageHeader from "../common/PageHeader.vue";

const summaryResource = createResource({
	url: "batwara.api.get_summary_for_session_user",
	auto: true,
	onSuccess(d) {
		console.log(d)
	}
})
</script>
