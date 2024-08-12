import { createRouter, createWebHistory } from 'vue-router'
import { session } from './data/session'
import { userResource } from '@/data/user'

const routes = [
	{
		path: '/',
		name: 'Dashboard',
		component: () => import('@/pages/Dashboard.vue'),
	},
	{
		path: '/friends',
		name: 'Friends',
		component: () => import('@/pages/Friends.vue'),
	},
	{
		path: '/new-expense',
		name: 'CreateExpense',
		component: () => import('@/pages/CreateNewExpense.vue'),
	},
	{
		path: '/login',
		name: 'Login',
		meta: {
			isLoginPage: true,
		},
		component: () => import('@/pages/LoginWithPhone.vue'),
	},
]

let router = createRouter({
	history: createWebHistory('/frontend'),
	routes,
})

router.beforeEach(async (to, from, next) => {
	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
	}

	if (!isLoggedIn && !to.meta.isLoginPage) {
		next({ name: 'Login' })
	}

	if (isLoggedIn && to.meta.isLoginPage) {
		next({ name: 'Dashboard' })
	}

	next()
})

export default router
