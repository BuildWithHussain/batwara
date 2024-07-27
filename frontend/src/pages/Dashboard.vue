<template>
	<div>
		<h2 class="font-bold text-gray-900 mb-4">Your friends</h2>

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
	</div>
</template>

<script setup>
import { computed } from "vue";
import { createListResource, Avatar } from "frappe-ui";
import { sessionUser } from "../data/session";

const friendsResource = createListResource({
	doctype: "Friend Mapping",
	fields: ["b as friend", "b.full_name as full_name", "b.user_image as user_image"
	],
	filters: {
		"a": sessionUser()
	},
	orderBy: "b",
	auto: true,
})

const friends = computed(() => {
	return friendsResource.list.data || [];
})
</script>
