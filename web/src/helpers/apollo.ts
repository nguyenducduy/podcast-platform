import Vue from "vue";
import ApolloClient from "apollo-client";
import { createUploadLink } from "apollo-upload-client";
import { InMemoryCache } from "apollo-cache-inmemory";
import { onError } from "apollo-link-error";
import VueApollo from "vue-apollo";

const getHeaders = () => {
  const headers = {};
  const token = Vue.ls.get("Access-Token");
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
};

// Error Handling
const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors)
    graphQLErrors.map(({ message, locations, path }) =>
      console.log(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
      )
    );
  if (networkError) console.log(`[Network error]: ${networkError}`);
});

const client = new ApolloClient({
  link: errorLink.concat(
    createUploadLink({
      uri: `${process.env.VUE_APP_GRAPHQL_URI}`,
      headers: getHeaders()
    })
  ),
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
