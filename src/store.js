import { createStore } from 'vuex';

const store = createStore({
  state: {
    accessToken: null,
    refreshToken: null,
    tokenExpiration: null,
    state: null,
  },
  mutations: {
    SET_ACCESS_TOKEN(state, data) {
      state.accessToken = data;
    },
    SET_REFRESH_TOKEN(state, data) {
      state.refreshToken = data;
    },
    SET_TOKEN_EXPIRATION(state, data) {
      state.tokenExpiration = data;
    },
    SET_STATE(state, data) {
      state.state = data;
    },
  },
  actions: {
    setAccessToken({ commit }, data) {
      commit('SET_ACCESS_TOKEN', data);
    },
    setRefreshToken({ commit }, data) {
      commit('SET_REFRESH_TOKEN', data);
    },
    setTokenExpiration({ commit }, data) {
      commit('SET_TOKEN_EXPIRATION', data);
    },
    setState({ commit }, data) {
      commit('SET_STATE', data);
    },
  },
  getters: {
    getAccessToken(state) {
      return state.accessToken;
    },
    getRefreshToken(state) {
      return state.refreshToken;
    },
    getTokenExpiration(state) {
      return state.tokenExpiration;
    },
    getState(state) {
      return state.state;
    },
  },
});

export default store;