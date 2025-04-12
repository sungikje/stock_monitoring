import { createStore } from "vuex";

const store = createStore({
  state() {
    return {
      accessToken: localStorage.getItem("access_token") || null,
    };
  },
  mutations: {
    setAccessToken(state, token) {
      state.accessToken = token;
      localStorage.setItem("access_token", token); // token을 localStorage에 저장
    },
    removeAccessToken(state) {
      state.accessToken = null;
      localStorage.removeItem("access_token"); // localStorage에서 삭제
    },
  },
  actions: {
    user_login({ commit }, token) {
      commit("setAccessToken", token);
    },
    user_logout({ commit }) {
      commit("removeAccessToken");
    },
  },
});

export default store;