import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from "../views/RegisterView.vue";
import LoginView from "../views/LoginView.vue";

const state = {
  token: localStorage.getItem('user-token') || '',
  status: '',
}

const getters = {
  isAuthenticated: !!state.token,
  authStatus: state.status,
}

const ifNotAuthenticated = (to, from, next) => {
  if (!getters.isAuthenticated) {
    next()
    return
  }
  next('/')
}

const ifAuthenticated = (to, from, next) => {
  if (getters.isAuthenticated) {
    next()
    return
  }
  next('/login')
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      beforeEnter: ifNotAuthenticated,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      beforeEnter: ifNotAuthenticated,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
