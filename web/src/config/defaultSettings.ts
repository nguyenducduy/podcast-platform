export default {
  production:
    process.env.NODE_ENV === "production" &&
    process.env.VUE_APP_PREVIEW !== "true",
  // vue-ls options
  storageOptions: {
    namespace: "podcast_olli__", // key prefix
    name: "ls", // name variable Vue.[ls] or this.[$ls],
    storage: "local" // storage name session, local, memory
  }
};
