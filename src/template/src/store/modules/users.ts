import { setToken } from "@/helpers/auth";

const state: any = {
  auth: null
};

const mutations: any = {
  SET_AUTH(state, { token, user }) {
    state.auth = {
      user: user,
      token: token
    };
    setToken(token);
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
