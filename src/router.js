import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import CallbackHandler from './components/CallbackHandler.vue'
import FindSongs from './components/FindTracks.vue'
import TopTracks from './components/TopTracks.vue';
// import TopArtists from './components/TopArtists.vue';

const routes = [
  { path: '/', component: HomePage, meta: { title: 'Sonaro' }},
  { path: '/callback', component: CallbackHandler },
  { path: '/findtracks', component: FindSongs },
  { path: '/toptracks', component: TopTracks },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  document.title = to.meta?.title ?? 'Sonaro'
})

export default router;