import gql from "graphql-tag";

export const GET_USERS = gql`
  query userList($first: Int, $last: Int, $sort: [UserNodeSortEnum]) {
    userList(first: $first, last: $last, sort: $sort) {
      totalCount
      edges {
        node {
          id
          fullName
          email
          avatar
          createdAt
          group {
            id
            screenName
            color
          }
        }
      }
    }
  }
`;

export const GET_USER = gql`
  query user($id: Int) {
    user(id: $id) {
      id
      fullName
      email
      group {
        id
        screenName
      }
    }
  }
`;

export const CREATE_USER = gql`
  mutation createUser(
    $fullName: String!
    $email: String!
    $password: String!
    $groupId: Int!
  ) {
    createUser(
      fullName: $fullName
      email: $email
      password: $password
      groupId: $groupId
    ) {
      user {
        id
        fullName
        email
      }
    }
  }
`;

export const UPDATE_USER = gql`
  mutation updateUser(
    $id: Int!
    $fullName: String!
    $email: String!
    $groupId: Int!
  ) {
    updateUser(id: $id, fullName: $fullName, email: $email, groupId: $groupId) {
      user {
        id
        fullName
        email
      }
    }
  }
`;

export const DELETE_USER = gql`
  mutation deleteUser($id: Int!) {
    deleteUser(id: $id) {
      deleted
    }
  }
`;

export const LOGIN_BY_EMAIL = gql`
  mutation loginUser($email: String!, $password: String!) {
    loginUser(email: $email, password: $password) {
      user {
        id
        email
        fullName
        createdAt
        group {
          id
          screenName
          color
        }
      }
      token
    }
  }
`;

export const LOGOUT_USER = gql`
  mutation logoutUser {
    logoutUser {
      loggedOut
    }
  }
`;

export const CHANGE_PASSWORD = gql`
  mutation changePassword($password: String!) {
    changePassword(password: $password) {
      user {
        id
        fullName
      }
    }
  }
`;
