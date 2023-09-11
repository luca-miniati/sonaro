import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import CallbackHandler from './components/CallbackHandler.vue'
import FindSongs from './components/FindSongs.vue'
import TopTracks from './components/TopTracks.vue';
// import TopArtists from './components/TopArtists.vue';

const routes = [
  { path: '/', component: HomePage, meta: { title: 'Spotify Playground' }},
  { path: '/callback', component: CallbackHandler },
  { path: '/findsongs', component: FindSongs },
  { path: '/toptracks', component: TopTracks },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  document.title = to.meta?.title ?? 'Spotify Playground'
})

export default router;