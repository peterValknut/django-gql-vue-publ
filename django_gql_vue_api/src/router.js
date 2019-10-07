import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Kartoteka from './components/Kartoteka'
import Grants from './components/Grants'

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'kartoteka',
      component: Kartoteka
    },
    {
      path: '/kartoteka',
      name: 'kartoteka',
      component: Kartoteka
    },
    {
      path: '/grants',
      name: 'grants',
      component: Grants
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    }
  ]
})
