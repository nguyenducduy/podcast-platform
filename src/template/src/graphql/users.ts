import gql from "graphql-tag";

export const GET_USERS = gql`
  query userList($first: Int, $last: Int) {
    viewer {
      userList(first: $first, last: $last, sort: [ID_ASC]) {
        totalCount
        groupList {
          text
          value
        }
        edges {
          node {
            id
            fullName
            groupId
            avatar
            createdAt
            group {
              text
              value
            }
          }
        }
        pageInfo {
          startCursor
          endCursor
          hasNextPage
          hasPreviousPage
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
