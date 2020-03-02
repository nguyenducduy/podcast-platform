import gql from "graphql-tag";

export const UPLOAD = gql`
  mutation filedriveUpload($file: Upload) {
    filedriveUpload(uploadFile: $file) {
      path
    }
  }
`;

export const UPLOAD_COMMON = gql`
  mutation commonUpload($file: Upload) {
    commonUpload(uploadFile: $file) {
      path
    }
  }
`;

export const RECORD_UPLOAD = gql`
  mutation recordUpload($file: Upload) {
    recordUpload(recordFile: $file) {
      path
    }
  }
`;

export const GET_ALL_FILEDRIVE = gql`
  query allFiledriveList($first: Int, $last: Int) {
    filedriveList(first: $first, last: $last, sort: [ID_DESC]) {
      totalCount
      edges {
        node {
          id
          name
          size
          duration
          path
          type {
            text
            value
            color
          }
          isCommon {
            text
            value
            color
          }
          createdAt
        }
      }
    }
  }
`;

export const GET_COMMON_FILEDRIVE = gql`
  query commonFiledriveList($first: Int, $last: Int) {
    filedriveList(
      first: $first
      last: $last
      sort: [ID_ASC]
      filters: { isTmp: 3, isCommon: 1 }
    ) {
      totalCount
      edges {
        node {
          id
          name
          size
          duration
          path
          type {
            text
            value
            color
          }
        }
      }
    }
  }
`;

export const GET_USER_FILEDRIVE = gql`
  query userFiledriveList($first: Int, $last: Int) {
    filedriveList(
      first: $first
      last: $last
      sort: [ID_DESC]
      filters: { isCommon: 3, isOwner: true }
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
          type {
            text
            value
            color
          }
        }
      }
    }
  }
`;

export const GET_FILES_TO_MIX = gql`
  query filedriveList($first: Int, $fromTrack: ID!, $toTrack: ID!) {
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
`;
