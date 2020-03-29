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
  }
};

const actions: any = {};

const getters: any = {
  loggedIn(state) {
    return !!state.auth || false;
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
