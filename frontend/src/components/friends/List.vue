<template>
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

<div v-else>
	You have not invited your friends yet.
</div>
</template>

<script setup>
import { inject } from "vue";
import { Avatar } from "frappe-ui";
import PageHeader from "../common/PageHeader.vue";

const friends = inject("friends");
</script>
