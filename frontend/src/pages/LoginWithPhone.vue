<template>
	<Card>
	<div class="flex items-center justify-center mb-8">
		<TabButtons :buttons="[
			{
				label: 'Login',
				value: 'login'
			},
			{
				label: 'Register',
				value: 'register'
			}
		]" v-model="selectedTab" />
	</div>

	<div v-if="selectedTab === 'login'">
		<div class="space-y-3">
			<FormControl :disabled="otpSent" v-model="phone" type="tel" label="Phone Number" placeholder="Phone" />

			<Button :disabled="otpSent" :loading="sendOTPResource.loading" @click="sendOTPResource.submit()" variant="outline" theme="green">Get OTP</Button>
		</div>

		<div class="mt-5 space-y-3" v-if="otpSent">
			<OTPInput v-model="otp" :disabled="verifyOTPResource.loading" @complete="handleOnOTPComplete" />
			<LoadingText v-if="verifyOTPResource.loading" />
			<ErrorMessage :message="verifyOTPResource.error" />
		</div>
	</div>
	<SignUpForm v-else />
	</Card>
</template>

<script setup>
import { inject, ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { Card, TabButtons, FormControl, createResource, ErrorMessage, LoadingText } from "frappe-ui";
import SignUpForm from "../components/auth/SignUpForm.vue";
import OTPInput from "../components/auth/OTPInput.vue";

const session = inject("session");
const route = useRoute();
const router = useRouter();

const phone = ref("");
const otp = ref(null);
const otpSent = ref(false);
const selectedTab = ref("login");
const invitationCode = ref(null);


onMounted(() => {
	invitationCode.value  = route.query.code;
})

const sendOTPResource = createResource({
	"url": "batwara.api.send_otp",
	makeParams() {
		return {
			phone: phone.value
		}
	},
	onSuccess() {
		otpSent.value = true;
	}
})

const verifyOTPResource = createResource({
	url: 'batwara.api.verify_otp_and_login',
	makeParams() {
		return {
			phone: phone.value,
			otp: otp.value,
			invite_code: invitationCode.value
		}
	},
	onSuccess() {
		session.postLogin();
		router.replace({ name: "Dashboard" })
	}
})

function handleOnOTPComplete() {
	verifyOTPResource.submit();
}
</script>
