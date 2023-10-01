import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './components/HomePage.vue'
import CallbackHandler from './components/CallbackHandler.vue'
import FindTracks from './components/FindTracks.vue'
import RecommendedTracks from './components/RecommendedTracks.vue'

const routes = [
  { path: '/', component: HomePage, meta: { title: 'Sonaro' }},
  { path: '/callback', component: CallbackHandler },
  { path: '/findtracks', component: FindTracks, meta: { title: 'Sonaro' }},
  {
    path: '/recommendedtracks/:tracks',
    name: 'recommendedtracks',
    component: RecommendedTracks,
    meta: { title: 'Sonaro' },
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  document.title = to.meta?.title ?? 'Sonaro'
})

export default router