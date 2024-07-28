<template>
  <div class="mx-4 my-2">
	<nav v-if="session.isLoggedIn">
		<ul>
			<li>
				<Button @click="session.logout.submit()" :loading="session.logout.loading">Log out</Button>
			</li>
		</ul>
	</nav>
    <router-view />
  </div>
</template>

<script setup>
import { computed, inject, provide, watch } from "vue";

import { getFriendsListResource } from "@/data/friends";

const session = inject("session");
const friendsList = getFriendsListResource();

watch(() => session.isLoggedIn, () => {
	friendsList.fetch();
})

const friends = computed(() => {
	return friendsList.list.data || [];
})

provide("friends", friends);
</script>
