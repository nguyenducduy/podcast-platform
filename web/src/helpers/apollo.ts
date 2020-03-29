import Vue from "vue";
import ApolloClient from "apollo-client";
import { createUploadLink } from "apollo-upload-client";
import { InMemoryCache } from "apollo-cache-inmemory";
import VueApollo from "vue-apollo";

const getHeaders = () => {
  const headers = {};
  const token = Vue.ls.get("Access-Token");
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
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

export default apolloProvider;
