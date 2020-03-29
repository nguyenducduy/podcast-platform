import Vue from "vue";

export default function({ next, context, store }) {
  const loggedToken = Vue.ls.get("Access-Token");

  if (!loggedToken) {
    return next({
      path: "/login",
      query: { redirect: context.to.fullPath }
    });
  }

  store.commit("users/SET_AUTH", {
    token: loggedToken
  });

  return next();
}
