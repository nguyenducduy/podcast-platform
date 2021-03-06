import gql from "graphql-tag";

export const GET_EPISODES = gql`
  query episodeList(
    $first: Int
    $last: Int
    $podcastId: Int!
    $sort: [EpisodeNodeSortEnum]
  ) {
    episodeList(
      first: $first
      last: $last
      sort: $sort
      filters: { pId: $podcastId }
    ) {
      totalCount
      edges {
        node {
          id
          title
          description
          status
          type
          cover
          orderNo
          seasonNo
          link
          author
          audioFile {
            id
            name
            path
          }
          externalFilePath
          createdAt
        }
      }
    }
  }
`;

export const GET_EPISODE = gql`
  query episode($id: Int) {
    episode(id: $id) {
      id
      title
      description
      status
      type
      cover
      orderNo
      seasonNo
      link
      author
      audioFile {
        id
        name
        path
      }
      createdAt
    }
  }
`;

export const CREATE_EPISODE = gql`
  mutation createEpisode(
    $pId: Int!
    $title: String!
    $description: String
    $status: Int!
    $type: Int!
    $orderNo: Int
    $seasonNo: Int
    $link: String
    $author: String
    $file: Upload
    $fdId: Int
  ) {
    createEpisode(
      pId: $pId
      title: $title
      description: $description
      status: $status
      type: $type
      orderNo: $orderNo
      seasonNo: $seasonNo
      link: $link
      author: $author
      coverImg: $file
      fdId: $fdId
    ) {
      episode {
        id
        title
      }
    }
  }
`;

export const UPDATE_EPISODE = gql`
  mutation updateEpisode(
    $episodeId: Int!
    $title: String!
    $description: String
    $status: Int!
    $type: Int!
    $orderNo: Int
    $seasonNo: Int
    $link: String
    $author: String
    $file: Upload
    $fdId: Int
  ) {
    updateEpisode(
      episodeId: $episodeId
      title: $title
      description: $description
      status: $status
      type: $type
      orderNo: $orderNo
      seasonNo: $seasonNo
      link: $link
      author: $author
      coverImg: $file
      fdId: $fdId
    ) {
      episode {
        id
        title
      }
    }
  }
`;

export const DELETE_EPISODE = gql`
  mutation deleteEpisode($episodeId: Int!) {
    deleteEpisode(episodeId: $episodeId) {
      deleted
    }
  }
`;
