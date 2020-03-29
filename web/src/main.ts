declare module "vue/types/vue" {
  // Global properties can be declared
  // on the `VueConstructor` interface
  interface VueConstructor {
    $axios: any;
    router: any;
    ls: any;
  }
  interface Vue {
    $axios: any;
    router: any;
    ls: any;
  }
}

import "core-js/stable";
import "regenerator-runtime/runtime";

import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import bootstrap from "./core/bootstrap";
import "./core/lazy_use";
import apolloProvider from "./helpers/apollo";

import NProgress from "vue-nprogress";
Vue.use(NProgress);
const nprogress = new NProgress({ parent: "body" });

import VuePageTitle from "vue-page-title";
Vue.use(VuePageTitle, {
  prefix: "Podcast | ",
  router
});

// import db from './utils/db';
// (async() => {
//   await db;
// })

Vue.config.productionTip = false;

new Vue({
  nprogress,
  router,
  store,
  apolloProvider,
  created: bootstrap,
  render: h => h(App)
} as any).$mount("#app");
