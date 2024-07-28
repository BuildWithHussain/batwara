import router from '@/router'
import { computed, reactive } from 'vue'
import { createResource } from 'frappe-ui'

import { userResource } from './user'

export function sessionUser() {
  const cookies = new URLSearchParams(document.cookie.split('; ').join('&'))
  let _sessionUser = cookies.get('user_id')
  if (_sessionUser === 'Guest') {
    _sessionUser = null
  }
  return _sessionUser
}

export const session = reactive({
  login: createResource({
    url: 'login',
    makeParams({ email, password }) {
      return {
        usr: email,
        pwd: password,
      }
    },
    onSuccess(data) {
	  this.postLogin();
      router.replace(data.default_route || '/')
    },
  }),
  postLogin() {
	userResource.reload()
	session.user = sessionUser()
	session.login.reset()
  },
  logout: createResource({
    url: 'logout',
    onSuccess() {
      userResource.reset()
      session.user = sessionUser()
      router.replace({ name: 'Login' })
    },
  }),
  user: sessionUser(),
  isLoggedIn: computed(() => !!session.user),
})
