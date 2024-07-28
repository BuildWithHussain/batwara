<template>
<PageHeader heading="Your friends">
	<template #actions>
		<Button variant="outline" @click="showInviteFriendsDialog = true">Invite friend</Button>
	</template>
</PageHeader>

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

<Dialog v-model="showInviteFriendsDialog" />
</template>

<script setup>
import { inject, ref } from "vue";
import { Avatar, Dialog } from "frappe-ui";
import PageHeader from "../common/PageHeader.vue";

const showInviteFriendsDialog = ref(false);

const friends = inject("friends");
</script>
