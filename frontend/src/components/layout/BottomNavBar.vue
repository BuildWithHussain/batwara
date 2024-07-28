<template>
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
import {inject} from "vue";
import { FeatherIcon } from "frappe-ui";

const session = inject("session");
</script>
