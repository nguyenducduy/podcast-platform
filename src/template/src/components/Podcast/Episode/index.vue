<template>
  <a-modal destroyOnClose :maskClosable="false" v-model="visible" width="1280px" :footer="null">
    <div slot="title">
      Podcast #{{ podcastId }} - Danh sách Episode ({{ pagination.total }})
      <a-button
        type="primary"
        icon="plus"
        size="small"
        class="float-right mr-10"
        @click="onOpenEpisodeAddModal(podcastId)"
      >Thêm</a-button>
    </div>
    <div class="row">
      <div class="col-lg-12">
        <a-table
          :dataSource="episodesGraph.edges"
          :columns="columns"
          :pagination="pagination"
          size="small"
          :rowKey="record => record.node.id"
          :loading="$apollo.loading"
          @change="onPageChange"
        >
          <a slot="_id" slot-scope="value" class="utils__link--underlined">{{ value }}</a>
          <a slot="_cover" slot-scope="record" :class="$style.thumbnail">
            <img
              :src="`${mediaUri}/${record.node.cover}`"
              onerror="this.onerror=null;this.src='/images/no-img.png';"
            />
          </a>
          <template slot="_title" slot-scope="record">
            <a class="text-xl">{{ record.node.title }}</a>
            <p class="text-sm text-gray-600">
              {{
              record.node.createdAt | moment("dddd, Do MMMM YYYY, h:mm:ss a")
              }}
            </p>
          </template>
          <p
            slot="_description"
            slot-scope="record"
            :class="$style.truncate"
            style="width: 250px;"
            v-html="record.node.description"
          ></p>
          <p slot="_orderNo" slot-scope="value" class="text-center">{{ value }}</p>
          <a-tag
            slot="_status"
            slot-scope="value"
            :color="value === 1 ? `#87d068` : ``"
          >{{ value === 1 ? "Xuất bản" : "Nháp" }}</a-tag>
          <a-tag
            slot="_type"
            slot-scope="value"
            :color="value === 1 ? `#87d068` : ``"
          >{{ getTypeName(value) }}</a-tag>
          <span slot="_actions" slot-scope="record">
            <inline-player :url="record.node.externalFilePath" />
            <a-tooltip title="Tải audio về máy chủ" v-if="record.node.audioFile === null">
              <a-button
                type="link"
                icon="download"
                size="small"
                class="mr-1"
                @click="onDownloadToServer(record.node.id)"
              ></a-button>
            </a-tooltip>
            <a-tooltip title="Đã tải" v-else>
              <a-icon
                type="check"
                class="focus:outline-none focus:shadow-outline text-teal-500 hover:text-teal-600 mr-2"
              ></a-icon>
            </a-tooltip>
            <a-tooltip title="Sửa">
              <a-button
                type="link"
                icon="edit"
                size="small"
                class="mr-1"
                @click="onOpenEditModal(record.node.id)"
              ></a-button>
            </a-tooltip>
            <a-popconfirm
              title="Chắn chắc xoá?"
              okText="Xoá"
              cancelText="Huỷ"
              placement="left"
              @confirm="onDelete(record.node.id)"
            >
              <a-tooltip title="Xoá">
                <a-button type="link" size="small">
                  <a-icon type="delete" />
                </a-button>
              </a-tooltip>
            </a-popconfirm>
          </span>
        </a-table>
      </div>
    </div>
    <episode-add-modal></episode-add-modal>
    <episode-edit-modal></episode-edit-modal>
  </a-modal>
</template>

<script lang="ts">
import { Vue, Component, Provide, Prop } from "vue-property-decorator";
import { bus } from "@/helpers/utils";
import { GET_EPISODES, DELETE_EPISODE } from "@/graphql/episodes";
import EpisodeAddModal from "@/components/Podcast/Episode/add.vue";
import EpisodeEditModal from "@/components/Podcast/Episode/edit.vue";
import InlinePlayer from "@/components/InlinePlayer/index.vue";

@Component({
  name: "episode-page",
  components: {
    EpisodeAddModal,
    EpisodeEditModal,
    InlinePlayer
  },
  apollo: {
    episodesGraph: {
      query: GET_EPISODES,
      variables() {
        return {
          first: this.pagination.pageSize,
          last: this.pagination.pageSize,
          podcastId: this.podcastId
        };
      },
      update(data) {
        return data.episodeList;
      },
      result({ data }) {
        this.pagination.total = data.episodeList.totalCount;
      },
      skip() {
        return this.skipQuery;
      },
      error(error) {
        this.$notification.error({
          message: "Fail to fetch episodeList!",
          description: error.toString(),
          duration: 5
        });
      }
    }
  }
})
export default class EpisodePage extends Vue {
  mediaUri: any = process.env.VUE_APP_MEDIA_URI;
  visible: boolean = false;
  podcastId: number = 0;

  // graphQL
  episodesGraph: any = {
    edges: []
  };
  skipQuery: boolean = true;
  // pagination
  pagination: any = {
    total: 0,
    pageSize: 10,
    showQuickJumper: true,
    hideOnSinglePage: true
  };
  // data table
  columns: any = [
    {
      title: "#",
      dataIndex: "node.id",
      sorter: (a, b) => a.node.id - b.node.id,
      scopedSlots: {
        customRender: "_id"
      }
    },
    {
      scopedSlots: {
        customRender: "_cover"
      }
    },
    {
      title: "Tiêu đề",
      scopedSlots: {
        customRender: "_title"
      }
    },
    {
      title: "Mô tả / Tóm tắt",
      scopedSlots: {
        customRender: "_description"
      }
    },
    {
      title: "STT",
      dataIndex: "node.orderNo",
      scopedSlots: {
        customRender: "_orderNo"
      }
    },
    // {
    //   title: "Link",
    //   dataIndex: "node.link",
    //   scopedSlots: {
    //     customRender: "_link"
    //   }
    // },
    // {
    //   title: "Tác giả",
    //   dataIndex: "node.author",
    //   scopedSlots: {
    //     customRender: "_author"
    //   }
    // },
    // {
    //   title: "Season No",
    //   dataIndex: "node.seasonNo",
    //   scopedSlots: {
    //     customRender: "_seasonNo"
    //   }
    // },
    {
      title: "Trạng thái",
      width: "6%",
      dataIndex: "node.status",
      scopedSlots: {
        customRender: "_status"
      }
    },
    {
      title: "Loại",
      width: "6%",
      dataIndex: "node.type",
      scopedSlots: {
        customRender: "_type"
      }
    },
    {
      width: "14%",
      scopedSlots: {
        customRender: "_actions"
      }
    }
  ];

  getTypeName(value) {
    let name: string = "";
    switch (value) {
      case 1:
        name = "Full";
        break;
      case 3:
        name = "Trailer";
        break;
      case 5:
        name = "Bonus";
        break;
    }

    return name;
  }

  onOpenEpisodeAddModal(podcastId) {
    bus.$emit("episode:showAddModal", podcastId);
  }

  onOpenEditModal(episodeId) {
    bus.$emit("episode:showEditModal", episodeId);
  }

  async onDelete(episodeId) {
    try {
      const res = await this.$apollo.mutate({
        mutation: DELETE_EPISODE,
        variables: {
          episodeId: episodeId
        }
      });

      if (res && res.data.deleted !== null) {
        this.$notification.success({
          message: "Delete episode success!",
          description: episodeId,
          duration: 2
        });

        this.$apollo.queries.episodesGraph.skip = false;
        await this.$apollo.queries.episodesGraph.refetch();
      }
    } catch (error) {
      this.$notification.error({
        message: "Delete episode failed!",
        description: error.toString(),
        duration: 5
      });
      return;
    }
  }

  async onPageChange(pagination) {
    const totalPages = pagination.total / this.pagination.pageSize;

    await this.$apollo.queries.episodesGraph.fetchMore({
      variables: {
        first: this.pagination.pageSize * pagination.current,
        last:
          pagination.current > totalPages
            ? pagination.total % this.pagination.pageSize
            : this.pagination.pageSize
      },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        return {
          episodeList: fetchMoreResult.episodeList
        };
      }
    });
  }

  async mounted() {
    bus.$on("episode:showListModal", async podcastId => {
      this.podcastId = podcastId;
      this.$apollo.queries.episodesGraph.skip = false;
      await this.$apollo.queries.episodesGraph.refetch();
      this.visible = true;
    });
    bus.$on("episode:refresh", async () => {
      this.$apollo.queries.episodesGraph.skip = false;
      await this.$apollo.queries.episodesGraph.refetch();
    });
  }
}
</script>

<style lang="scss" module scoped>
@import "./index.module.scss";
</style>
