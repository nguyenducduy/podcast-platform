import gql from "graphql-tag";

export const GET_PODCASTS = gql`
  query podcastList($first: Int, $last: Int) {
    viewer {
      podcastList(first: $first, last: $last, sort: [ID_ASC]) {
        totalCount
        edges {
          node {
            id
            title
            description
            status
            cover
            contactEmail
            websiteUrl
            copyright
            createdAt
          }
        }
      }
    }
  }
`;

export const GET_PODCAST = gql`
  query podcast($id: Int) {
    viewer {
      podcast(id: $id) {
        id
        title
        description
        contactEmail
        websiteUrl
        copyright
        status
        cover
        createdAt
      }
    }
  }
`;

export const CREATE_PODCAST = gql`
  mutation createPodcast(
    $title: String!
    $description: String
    $status: Int!
    $file: Upload!
    $contactEmail: String
    $websiteUrl: String
    $copyright: String
  ) {
    createPodcast(
      title: $title
      description: $description
      status: $status
      coverImg: $file
      contactEmail: $contactEmail
      websiteUrl: $websiteUrl
      copyright: $copyright
    ) {
      podcast {
        id
        title
      }
    }
  }
`;

export const UPDATE_PODCAST = gql`
  mutation updatePodcast(
    $podcastId: Int!
    $title: String!
    $description: String
    $status: Int!
    $file: Upload
    $contactEmail: String
    $websiteUrl: String
    $copyright: String
  ) {
    updatePodcast(
      podcastId: $podcastId
      title: $title
      description: $description
      status: $status
      coverImg: $file
      contactEmail: $contactEmail
      websiteUrl: $websiteUrl
      copyright: $copyright
    ) {
      podcast {
        id
        title
      }
    }
  }
`;

export const DELETE_PODCAST = gql`
  mutation deletePodcast($podcastId: Int!) {
    deletePodcast(podcastId: $podcastId) {
      deleted
    }
  }
`;

export const IMPORT_FROM_APPLE = gql`
  mutation importFromApple($id: Int!) {
    importFromApple(id: $id) {
      imported
    }
  }
`;
