import { Vue } from "vue-property-decorator";
import VueRouter from "vue-router";
import store from "@/store";
import auth from "../middleware/auth";
// import log from "../middleware/log";

Vue.use(VueRouter);

let router = new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/login",
      component: require("@/views/Login/index").default,
      meta: {
        layout: "login"
      }
    },
    {
      path: "/",
      component: require("@/views/Home").default,
      meta: {
        middleware: [auth]
      }
    },
    {
      path: "/user",
      component: require("@/views/User/index").default,
      meta: {
        title: "User",
        middleware: [auth]
      }
    },
    {
      path: "/user/changepassword",
      component: require("@/views/User/changepassword").default,
      meta: {
        title: "User",
        middleware: [auth]
      }
    },
    {
      path: "/podcast",
      component: require("@/views/Podcast/index").default,
      meta: {
        title: "Podcast",
        middleware: [auth]
      }
    },
    {
      path: "/podcast/compose",
      component: require("@/views/Podcast/compose").default,
      meta: {
        middleware: [auth]
      }
    },
    {
      path: "/podcast/record",
      component: require("@/views/Podcast/record").default,
      meta: {
        middleware: [auth]
      }
    },
    {
      path: "/filedrive",
      component: require("@/views/Filedrive/index").default,
      meta: {
        middleware: [auth]
      }
    },
    {
      path: "*",
      redirect: "/"
    }
    // {
    //   path: "/install",
    //   name: "install-page",
    //   component: require("@/pages/InstallPage").default,
    //   meta: {
    //     middleware: [log],
    //     layout: "blank"
    //   }
    // },
  ]
});

router.beforeEach((to, from, next) => {
  if (!to.meta.middleware) {
    return next();
  }

  const middleware = Array.isArray(to.meta.middleware)
    ? to.meta.middleware
    : [to.meta.middleware];

  const context = {
    from,
    next,
    router,
    to
  };
  const nextMiddleware = nextFactory(context, middleware, 1);

  return middleware[0]({ context, next: nextMiddleware, store });
});

function nextFactory(context: any, middleware: any, index: any) {
  const subsequentMiddleware = middleware[index];
  // If no subsequent Middleware exists,
  // the default `next()` callback is returned.
  if (!subsequentMiddleware) return context.next;

  return (parameters: any) => {
    // Run the default Vue Router `next()` callback first.
    context.next(parameters);
    // Than run the subsequent Middleware with a new
    // `nextMiddleware()` callback.
    const nextMiddleware = nextFactory(context, middleware, index + 1);
    subsequentMiddleware({ context, next: nextMiddleware, store });
  };
}

export default router;
