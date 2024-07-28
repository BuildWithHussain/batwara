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

<Dialog :options="{ title: 'Invite Friend' }" v-model="showInviteFriendsDialog">
	<template #body-content>
		<div class="space-y-3">
			<FormControl v-model="inviteDetails.invitee_name" type="text" label="Name" placeholder="Jane Doe" />
			<FormControl v-model="inviteDetails.invitee_phone" type="tel" label="Mobile Number" />
		</div>

		<ErrorMessage :message="invitationListResource.insert.error" />
	</template>

	<template #actions>
		<Button
			:loading="invitationListResource.insert.loading"
			variant="solid"
			theme="green"
			@click="sendInvite">
			Send Invite
		</Button>
	</template>
</Dialog>
</template>

<script setup>
import { inject, ref, reactive } from "vue";
import { Avatar, createListResource, Dialog, FormControl } from "frappe-ui";
import PageHeader from "../common/PageHeader.vue";
import { sessionUser } from "@/data/session";

const showInviteFriendsDialog = ref(false);

const friends = inject("friends");

const inviteDetails = reactive({
	"invitee_name": "",
	"invitee_phone": ""
})

const invitationListResource = createListResource({
	doctype: "Friend Invitation"
})

function sendInvite() {
	invitationListResource.insert.submit({
		...inviteDetails,
		invited_by: sessionUser()
	}, {
		onSuccess() {
			showInviteFriendsDialog.value = false;
		}
	})
}
</script>
