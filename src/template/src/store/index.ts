import { Vue } from "vue-property-decorator";
import * as Vuex from "vuex";

import settings from "./modules/settings";
import users from "./modules/users";

Vue.use(Vuex);

export const state = {};

export const mutations = {
  SET(state, payload) {
    state[payload.app] = payload.value;
  }
};

export const getters = {
  openKeys(state) {
    return state["menu.openedKeys"] || [];
  },
  selectedKeys(state) {
    return state["menu.selectedKeys"] || [];
  }
};

export default new Vuex.Store({
  state,
  mutations,
  getters,
  modules: {
    settings,
    users
  },
  strict: process.env.NODE_ENV !== "production"
});
