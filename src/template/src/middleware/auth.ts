import {
  getTokenFromLocalStorage,
  getUserFromLocalStorage
} from "@/helpers/auth";

export default function({ next, context, store }) {
  const loggedToken = getTokenFromLocalStorage();
  const loggedUser = getUserFromLocalStorage();

  if (!loggedToken) {
    return next({
      path: "/login",
      query: { redirect: context.to.fullPath }
    });
  }

  // store.commit("users/SET_AUTH", {
  //   user: loggedUser,
  //   token: loggedToken
  // });

  return next();
}
