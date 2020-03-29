import gql from "graphql-tag";

export const GET_USERS = gql`
  query userList($first: Int, $last: Int, $sort: [UserNodeSortEnum]) {
    userList(first: $first, last: $last, sort: $sort) {
      totalCount
      edges {
        node {
          id
          fullName
          groupId
          avatar
          createdAt
          group {
            id
            name
            screenName
          }
        }
      }
    }
  }
`;

export const LOGIN_BY_EMAIL = gql`
  mutation loginUser($email: String!, $password: String!) {
    loginUser(email: $email, password: $password) {
      user {
        id
        fullName
      }
      token
    }
  }
`;
