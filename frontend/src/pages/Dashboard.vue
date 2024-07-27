<template>
	<div>
		<PageHeader heading="Your friends" />

		<div v-if="friends">
			<ol class="flex flex-col space-y-3">
				<li class="flex items-center space-x-2" v-for="friend in friends" :key="friend">
					<Avatar size="xl" :label="friend.full_name" :url="friend.user_image" />
					<div>
						{{ friend.full_name }}
					</div>
				</li>
			</ol>
		</div>

		<div class="mt-5">
			<Button route="/new-expense" variant="solid" theme="blue">+ Add Expense</Button>
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

	</div>
</template>

<script setup>
import { inject } from "vue";
import { Avatar, createResource, LoadingText } from "frappe-ui";

import PageHeader from "../components/common/PageHeader.vue";

const friends = inject("friends");

const summaryResource = createResource({
	url: "batwara.api.get_summary_for_session_user",
	auto: true,
	onSuccess(d) {
		console.log(d)
	}
})
</script>
