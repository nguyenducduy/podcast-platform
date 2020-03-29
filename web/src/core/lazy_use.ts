import { Vue } from "vue-property-decorator";
import VueStorage from "vue-ls";
import VueApollo from "vue-apollo";
import config from "@/config/defaultSettings";

// import base library
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import "../assets/global.scss";
import "../assets/styles/tailwind.css";
import VueNumerals from "vue-numerals";
import VueMoment from "vue-moment";
import moment from "moment-timezone";

Vue.use(VueStorage, config.storageOptions);
Vue.use(VueApollo);
Vue.prototype.$notification = Antd.notification;
Vue.use(Antd);
moment.locale("vi");
moment.tz.setDefault("Asia/Ho_Chi_Minh");
Vue.use(VueMoment, { moment });
Vue.use(VueNumerals);
