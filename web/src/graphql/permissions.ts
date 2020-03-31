import gql from "graphql-tag";

export const GET_PERMISSIONS = gql`
  query permissionList($first: Int, $last: Int) {
    permissionList(first: $first, last: $last, sort: [ID_ASC]) {
      totalCount
      edges {
        node {
          id
          name
          description
        }
      }
    }
  }
`;

export const GET_PERMISSION = gql`
  query permission($id: Int) {
    permission(id: $id) {
      id
      name
      description
    }
  }
`;

export const CREATE_PERMISSION = gql`
  mutation createPermission($name: String!, $description: String!) {
    createPermission(name: $name, description: $description) {
      permission {
        id
        name
        description
      }
    }
  }
`;

export const UPDATE_PERMISSION = gql`
  mutation updatePermission($id: Int!, $name: String!, $description: String!) {
    updatePermission(id: $id, name: $name, description: $description) {
      permission {
        id
        name
        description
      }
    }
  }
`;

export const DELETE_PERMISSION = gql`
  mutation deletePermission($id: Int!) {
    deletePermission(id: $id) {
      deleted
    }
  }
`;
