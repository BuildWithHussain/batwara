<template>
  <div class="mx-4 my-2">
	<nav class="flex justify-between items-center mb-6" v-if="session.isLoggedIn">
		<p class="font-semibold text-gray-900 text-xl">
			<span class="text-3xl mr-2">👛</span> batwara.app
		</p>

		<Button @click="session.logout.submit()" :loading="session.logout.loading">Log out</Button>
	</nav>
    <router-view />
  </div>

  <BottomNavBar />
</template>

<script setup>
import { computed, inject, provide, watch } from "vue";
import { getFriendsListResource } from "@/data/friends";
import BottomNavBar from "./components/layout/BottomNavBar.vue";

const session = inject("session");
const friendsList = getFriendsListResource();

watch(() => session.isLoggedIn, () => {
	friendsList.fetch();
})

const friends = computed(() => {
	return friendsList.data || [];
})

provide("friends", friends);
</script>
