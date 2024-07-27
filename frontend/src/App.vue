<template>
  <div class="mx-4 my-2">
    <router-view />
  </div>
</template>

<script setup>
import { computed, provide } from "vue";

import { getFriendsListResource } from "@/data/friends";

const friendsList = getFriendsListResource();

const friends = computed(() => {
	return friendsList.list.data || [];
})

provide("friends", friends);
</script>
