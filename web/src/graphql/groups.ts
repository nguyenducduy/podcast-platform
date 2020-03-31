import gql from "graphql-tag";

export const GET_GROUPS = gql`
  query groupList($first: Int, $last: Int) {
    groupList(first: $first, last: $last, sort: [ID_ASC]) {
      totalCount
      edges {
        node {
          id
          name
          screenName
          color
          createdAt
        }
      }
    }
  }
`;

export const GET_GROUP = gql`
  query group($id: Int) {
    group(id: $id) {
      id
      name
      screenName
      color
      permissions {
        id
        name
      }
    }
  }
`;

export const CREATE_GROUP = gql`
  mutation createGroup($name: String!, $screenName: String!, $color: String!) {
    createGroup(name: $name, screenName: $screenName, color: $color) {
      group {
        id
        name
        screenName
      }
    }
  }
`;

export const UPDATE_GROUP = gql`
  mutation updateGroup(
    $id: Int!
    $name: String!
    $screenName: String!
    $color: String!
  ) {
    updateGroup(id: $id, name: $name, screenName: $screenName, color: $color) {
      group {
        id
        name
        screenName
      }
    }
  }
`;

export const DELETE_GROUP = gql`
  mutation deleteGroup($id: Int!) {
    deleteGroup(id: $id) {
      deleted
    }
  }
`;

export const GRANT_PERMISSION = gql`
  mutation grantPermission($id: Int!, $permissions: [String]!) {
    grantPermission(id: $id, permissions: $permissions) {
      granted
    }
  }
`;
