import Vue from "vue";

const state: any = {
  auth: null
};

const mutations: any = {
  SET_AUTH(state, { token, user }) {
    state.auth = {
      user: user,
      token: token
    };

    Vue.ls.set("Access-Token", token);
    Vue.ls.set("Logged-User", user);
  },
  REMOVE_AUTH(state) {
    Vue.ls.remove("Access-Token");
    Vue.ls.remove("Logged-User");
  }
};

const actions: any = {};

const getters: any = {
  loggedIn(state) {
    return !!state.auth || false;
  },
  loggedUser(state) {
    return state.auth.user || null;
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
