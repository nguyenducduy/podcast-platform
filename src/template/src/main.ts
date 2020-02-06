import { Vue } from "vue-property-decorator";
import App from "./App.vue";
import Antd from "ant-design-vue";
import ApolloClient from "apollo-client";
import { createUploadLink } from "apollo-upload-client";
import { InMemoryCache } from "apollo-cache-inmemory";
import VueApollo from "vue-apollo";
import router from "./router";
import store from "./store";
import "ant-design-vue/dist/antd.css";
import "./assets/global.scss";
import NProgress from "vue-nprogress";
import VueNumerals from "vue-numerals";
import VueMoment from "vue-moment";
import moment from "moment-timezone";
import "./assets/styles/tailwind.css";
import { getTokenFromLocalStorage } from "@/helpers/auth";

import LoginLayout from "./layouts/Login/index.vue";
import MainLayout from "./layouts/Main/index.vue";

const getHeaders = () => {
  const headers: any = {};
  const token = getTokenFromLocalStorage();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
};


const client = new ApolloClient({
  link: createUploadLink({
    uri: `${process.env.VUE_APP_GRAPHQL_URI}`,
    headers: getHeaders()
  }),
  cache: new InMemoryCache(),
  connectToDevTools: true
});
const apolloProvider = new VueApollo({
  defaultClient: client,
  defaultOptions: {
    $loadingKey: "loading",
    $query: {
      fetchPolicy: "network-only"
    }
  }
});

// import db from './utils/db';
// (async() => {
//   await db;
// })

Vue.config.productionTip = false;
Vue.prototype.$notification = Antd.notification;
const nprogress = new NProgress({ parent: "body" });
Vue.component("login-layout", LoginLayout);
Vue.component("main-layout", MainLayout);
Vue.use(VueApollo);
Vue.use(Antd);
moment.locale("vi");
moment.tz.setDefault("Asia/Ho_Chi_Minh");
Vue.use(VueMoment, { moment });
Vue.use(VueNumerals);

new Vue({
  router,
  store,
  apolloProvider,
  render(createElement: any) {
    return createElement(App);
  }
} as any).$mount("#app");

console.info("App init successfull");
