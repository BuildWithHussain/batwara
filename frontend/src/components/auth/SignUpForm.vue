<template>
	<div class="mt-5 space-y-4">
		<div class="space-y-3">
			<FormControl v-model="signUpDetails.full_name" type="text" label="Full Name" placeholder="Jane Doe" />
			<FormControl v-model="signUpDetails.email" type="email" label="Email" placeholder="janedoe@email.com" />
			<FormControl v-model="signUpDetails.phone" type="phone" label="Phone" />

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
import { ref, reactive } from "vue";
import { FormControl, createResource, LoadingText, ErrorMessage } from "frappe-ui";
import OTPInput from "../auth/OTPInput.vue";

const signUpDetails = reactive({
	phone: null,
	otp: null,
	email: "",
	full_name: ""
})

const otpSent = ref(false);

const sendOTPResource = createResource({
	url: "batwara.api.send_otp",
	makeParams() {
		return {
			phone: signUpDetails.phone
		}
	},
	onSuccess() {
		otpSent.value = true;
	}
})

const verifyOTPAndRegister = createResource({
	url: "batwara.api.verify_otp_and_register",
	makeParams() {
		print({...signUpDetails})
		return {
			...signUpDetails
		}
	},
	onSuccess() {

	}
})

function handleOTPInputComplete() {
	verifyOTPAndRegister.submit()
}
</script>
