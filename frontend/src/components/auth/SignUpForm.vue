<template>
	<div class="mt-5 space-y-4">
		<div class="space-y-3">
			<FormControl v-model="signUpDetails.full_name" type="text" label="Full Name" placeholder="Jane Doe" />
			<FormControl v-model="signUpDetails.email" type="email" label="Email" placeholder="janedoe@email.com" />

			<div class="flex justify-center items-end">
				<FormControl class="shrink-0 w-24" disabled type="select" value="+91" :options="[
					{
						value: '+91',
						label: '+91'
					}
				]" />
				<FormControl class="w-full" v-model="signUpDetails.phone" type="tel" label="Phone Number" placeholder="Phone" />
			</div>

			<Button :disabled="otpSent" :loading="sendOTPResource.loading" @click="sendOTPResource.submit()" variant="outline" theme="green">Get OTP</Button>
		</div>

		<div v-if="verifyOTPAndRegister.loading">
			<LoadingText />
		</div>

		<div>
			<ErrorMessage :message="verifyOTPAndRegister.error || sendOTPResource.error" />
		</div>

		<div v-if="otpSent">
			<OTPInput
				v-model="signUpDetails.otp"
				:disabled="verifyOTPAndRegister.loading"
				@complete="handleOTPInputComplete"
			/>
		</div>
	</div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from "vue";
import { FormControl, createResource, LoadingText, ErrorMessage } from "frappe-ui";
import OTPInput from "../auth/OTPInput.vue";
import { useRoute } from "vue-router";


const session = inject("session");

const signUpDetails = reactive({
	phone: null,
	otp: null,
	email: "",
	full_name: "",
	invite_code: null
})

const route = useRoute();
onMounted(() => {
	signUpDetails.invite_code = route.query.code;
})

const otpSent = ref(false);

const sendOTPResource = createResource({
	url: "batwara.api.send_otp",
	makeParams() {
		return {
			phone: "+91" + signUpDetails.phone
		}
	},
	onSuccess() {
		otpSent.value = true;
	}
})

const verifyOTPAndRegister = createResource({
	url: "batwara.api.verify_otp_and_register",
	makeParams() {
		return {
			...signUpDetails,
			phone: "+91" + signUpDetails.phone
		}
	},
	onSuccess() {
		session.postLogin();
	}
})

function handleOTPInputComplete() {
	verifyOTPAndRegister.submit()
}
</script>
