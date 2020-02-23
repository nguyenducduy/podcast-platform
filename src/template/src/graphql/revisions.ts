import gql from "graphql-tag";

export const GET_REVISIONS = gql`
  query revisionList(
    $first: Int
    $last: Int
    $sessionId: String
    $version: Int
  ) {
    viewer {
      revisionList(
        first: $first
        last: $last
        sort: [VERSION_DESC]
        filters: { sessionId: $sessionId, isOwner: true, version: $version }
      ) {
        totalCount
        edges {
          cursor
          node {
            id
            sessionId
            uId
            content
            filesUsed
            version
            mixedFile {
              id
              path
            }
          }
        }
      }
    }
  }
`;

export const GET_HISTORIES = gql`
  query historyList($first: Int, $last: Int) {
    viewer {
      historyList(
        first: $first
        last: $last
        sort: [CREATED_AT_DESC, SESSION_ID_DESC, VERSION_DESC]
        filters: { isOwner: true }
      ) {
        totalCount
        edges {
          cursor
          node {
            id
            sessionId
            uId
            content
            filesUsed
            version
            createdAt
            mixedFile {
              id
              path
            }
          }
        }
      }
    }
  }
`;

export const CREATE_REVISION = gql`
  mutation createRevision($content: String!, $sessionId: String!) {
    createRevision(sessionId: $sessionId, content: $content) {
      revision {
        id
        version
      }
      tmpFile
    }
  }
`;

export const DETACH_REVISION = gql`
  mutation detachRevision(
    $sessionId: String!
    $version: Int!
    $detachIndex: Int!
  ) {
    detachRevision(
      sessionId: $sessionId
      version: $version
      detachIndex: $detachIndex
    ) {
      revision {
        id
        version
      }
    }
  }
`;

export const CHANGE_FILE_ORDER_IN_REVISION = gql`
  mutation changeFileOrderInRevision(
    $newTracksOrder: String!
    $sessionId: String!
    $version: Int!
  ) {
    changeFileOrderInRevision(
      newTracksOrder: $newTracksOrder
      sessionId: $sessionId
      version: $version
    ) {
      revision {
        id
        version
      }
    }
  }
`;
