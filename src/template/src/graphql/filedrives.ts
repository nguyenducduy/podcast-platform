import gql from "graphql-tag";

export const UPLOAD = gql`
  mutation filedriveUpload($file: Upload) {
    filedriveUpload(uploadFile: $file) {
      path
    }
  }
`;

export const GET_COMMON_FILEDRIVE = gql`
  query commonFiledriveList($first: Int, $last: Int) {
    viewer {
      filedriveList(
        first: $first
        last: $last
        sort: [ID_ASC]
        filters: {
          isTmp: 3
          # isCommon: 1,
          typeIn: [1, 3]
        }
      ) {
        totalCount
        edges {
          cursor
          node {
            id
            name
            size
            duration
            path
            type
          }
        }
      }
    }
  }
`;

export const GET_FILES_TO_MIX = gql`
  query filedriveList($first: Int, $fromTrack: ID!, $toTrack: ID!) {
    viewer {
      filedriveList(
        first: $first
        sort: [ID_DESC]
        filters: { idIn: [$fromTrack, $toTrack] }
      ) {
        totalCount
        edges {
          node {
            id
            name
            size
            duration
            path
          }
        }
      }
    }
  }
`;
