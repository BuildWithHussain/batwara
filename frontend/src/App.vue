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

  <nav v-if="session.isLoggedIn" class="absolute bottom-0 w-full bg-gray-100 py-2 px-8">
	<ul class="flex justify-around items-center">
		<li>
			<RouterLink :to="{name: 'Dashboard'}" v-slot="{ isExactActive }">
				<FeatherIcon
					:class="[
						'w-6',
						isExactActive ? 'text-gray-700' : 'text-gray-500'
					]"
					name="home" />
			</RouterLink>
		</li>

		<li>
			<Button :route="{ name: 'CreateExpense' }" theme="green" variant="solid" size="xl" icon="plus" />
		</li>

		<li>
			<RouterLink :to="{name: 'Friends'}" v-slot="{ isExactActive }">
				<FeatherIcon
					:class="[
						'w-6',
						isExactActive ? 'text-gray-700' : 'text-gray-500'
					]"
					name="users" />
			</RouterLink>
		</li>
	</ul>
  </nav>
</template>

<script setup>
import { computed, inject, provide, watch } from "vue";
import { FeatherIcon } from "frappe-ui";
import { getFriendsListResource } from "@/data/friends";

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
