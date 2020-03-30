import { Vue } from "vue-property-decorator";
import VueRouter from "vue-router";
import store from "@/store";
import MainLayout from "@/layouts/Main/index.vue";
import LoginLayout from "@/layouts/Login/index.vue";

Vue.use(VueRouter);

let router = new VueRouter({
  base: process.env.BASE_URL,
  mode: "history",
  routes: [
    {
      path: "/admin",
      redirect: "admin/dashboard",
      component: MainLayout,
      meta: {
        authRequired: true
      },
      children: [
        {
          path: "/admin/dashboard",
          meta: {
            title: "Dashboard"
          },
          component: require("@/views/Home").default
        },
        {
          path: "/admin/user",
          meta: {
            title: "User"
          },
          component: require("@/views/User/index").default
        },
        {
          path: "/admin/podcast",
          meta: {
            title: "Podcast"
          },
          component: require("@/views/Podcast/index").default
        },
        {
          path: "/admin/podcast/compose",
          meta: {
            title: "Podcast compose"
          },
          component: require("@/views/Podcast/compose").default
        },
        {
          path: "/admin/filedrive",
          meta: {
            title: "Filedrive"
          },
          component: require("@/views/Filedrive/index").default
        }
      ]
    },

    // Non perm pages
    {
      path: "/admin/login",
      component: LoginLayout,
      children: [
        {
          path: "/admin/login",
          meta: {
            title: "Login"
          },
          component: require("@/views/Login/index").default
        }
        // {
        //   path: '/admin/forgot',
        //   meta: {
        //     title: 'Forgot Password',
        //   },
        //   component: () => import('./views/user/forgot'),
        // },
      ]
    },

    // 404
    {
      path: "/404",
      meta: {
        title: "404"
      },
      component: require("@/views/404").default
    },

    // Redirect to 404
    {
      path: "*",
      redirect: "/404"
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.authRequired)) {
    const loggedToken = Vue.ls.get("Access-Token");

    if (!loggedToken) {
      return next({
        path: "/admin/login",
        query: { redirect: to.fullPath }
      });
    }

    store.commit("users/SET_AUTH", {
      token: loggedToken
    });

    next();
  } else {
    next();
  }
});

export default router;
