import gql from "graphql-tag";

export const GET_USERS = gql`
  query userList($first: Int, $last: Int, $sort: [UserNodeSortEnum]) {
    userList(first: $first, last: $last, sort: $sort) {
      totalCount
      edges {
        node {
          id
          fullName
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

export const GET_USER = gql`
  query user($id: Int) {
    user(id: $id) {
      id
    }
  }
`;

// export const CREATE_USER = gql`
//   mutation createGroup($name: String!, $screenName: String!, $color: String!) {
//     createGroup(name: $name, screenName: $screenName, color: $color) {
//       group {
//         id
//         name
//         screenName
//       }
//     }
//   }
// `;

// export const UPDATE_GROUP = gql`
//   mutation updateGroup(
//     $id: Int!
//     $name: String!
//     $screenName: String!
//     $color: String!
//   ) {
//     updateGroup(name: $name, screenName: $screenName, color: $color) {
//       group {
//         id
//         name
//         screenName
//       }
//     }
//   }
// `;

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
        fullName
      }
      token
    }
  }
`;
