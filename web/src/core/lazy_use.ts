import { Vue } from "vue-property-decorator";
import VueStorage from "vue-ls";
import VueApollo from "vue-apollo";
import config from "@/config/defaultSettings";

// import base library
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import "../assets/global.scss";
import "../assets/styles/tailwind.css";
import NProgress from "vue-nprogress";
import VueNumerals from "vue-numerals";
import VueMoment from "vue-moment";
import moment from "moment-timezone";

import LoginLayout from "../layouts/Login/index.vue";
import MainLayout from "../layouts/Main/index.vue";

Vue.use(VueStorage, config.storageOptions);
Vue.use(VueApollo);
Vue.prototype.$notification = Antd.notification;
const nprogress = new NProgress({ parent: "body" });
Vue.use(Antd);
moment.locale("vi");
moment.tz.setDefault("Asia/Ho_Chi_Minh");
Vue.use(VueMoment, { moment });
Vue.use(VueNumerals);
Vue.component("login-layout", LoginLayout);
Vue.component("main-layout", MainLayout);
