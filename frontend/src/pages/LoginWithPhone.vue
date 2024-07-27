<template>
	<PageHeader heading="Login with Phone" />

	<div class="space-y-3">
		<FormControl :disabled="otpSent" v-model="phone" type="tel" label="Phone Number" placeholder="Phone" />

		<Button :disabled="otpSent" :loading="sendOTPResource.loading" @click="sendOTPResource.submit()" variant="outline" theme="green">Send OTP</Button>
	</div>

	<div class="mt-5 space-y-3" v-if="otpSent">
		<VOtpInput
			input-classes="w-10 h-10 font-bold m-1 rounded border-gray-400 focus:border-0 focus:ring-2 focus:ring-green-500"
			:should-auto-focus="true"
			:should-focus-order="true"
			v-model="otp"
			separator="-"
			@on-change="handleOnOTPChange"
			@on-complete="handleOnOTPComplete"
			:placeholder="['*', '*', '*', '*', '*', '*']"
			:num-inputs="6"
			:is-disabled="verifyOTPResource.loading"
			 />

			 <LoadingText v-if="verifyOTPResource.loading" />

			 <ErrorMessage :message="verifyOTPResource.error" />
	</div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import VOtpInput from "vue3-otp-input";
import { FormControl, createResource, ErrorMessage, LoadingText } from "frappe-ui";
import PageHeader from "../components/common/PageHeader.vue"

const router = useRouter();

const phone = ref("");
const otp = ref(null);
const otpSent = ref(false);

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
			otp: otp.value
		}
	},
	onSuccess() {
		router.replace({name: "Dashboard"})
	}
})

function handleOnOTPComplete() {
	verifyOTPResource.submit();
}

function handleOnOTPChange(value) {
	otp.value = value;
}

</script>
