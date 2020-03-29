<template>
  <a-layout-content class="lg">
    <div class="utils__title mb-3">
      <strong class="text-uppercase font-size-16">Danh sách ({{ pagination.total }})</strong>
      <podcast-add />
      <a-button
        type="dashed"
        icon="link"
        class="float-right mr-2"
        @click="onOpenImportFromAppleModal()"
      >Import từ Apple Podcast</a-button>
    </div>
    <a-table
      :dataSource="podcastsGraph.edges"
      :columns="columns"
      :pagination="false"
      size="small"
      :rowKey="record => record.node.id"
      :loading="$apollo.loading"
    >
      <a slot="_id" slot-scope="value" class="utils__link--underlined">
        {{
        value
        }}
      </a>
      <a slot="_cover" slot-scope="record" :class="$style.thumbnail">
        <img
          :src="`${mediaUri}/${record.node.cover}`"
          onerror="this.onerror=null;this.src='/images/no-img.png';"
        />
      </a>
      <template slot="_title" slot-scope="record">
        <a class="text-xl" @click="onOpenEpisodeListModal(record.node.id)">
          <a-tooltip title="Nhấn để hiện danh sách Episode">
            {{
            record.node.title
            }}
          </a-tooltip>
        </a>
        <p
          class="text-sm text-gray-600"
        >{{ record.node.createdAt | moment("dddd, Do MMMM YYYY, h:mm:ss a") }}</p>
      </template>
      <p
        slot="_description"
        slot-scope="record"
        :class="$style.truncate"
        style="width: 250px;"
        v-html="record.node.description"
      ></p>
      <p slot="_contactEmail" slot-scope="value">{{ value }}</p>
      <p slot="_websiteUrl" slot-scope="value">{{ value }}</p>
      <p slot="_copyright" slot-scope="value">{{ value }}</p>
      <a-tag
        slot="_status"
        slot-scope="value"
        :color="value === 1 ? `#87d068` : ``"
      >{{ value === 1 ? "Xuất bản" : "Nháp" }}</a-tag>
      <span slot="_actions" slot-scope="record">
        <a-tooltip title="Danh sách Episode">
          <a-button
            type="link"
            icon="bars"
            size="small"
            class="mr-1"
            @click="onOpenEpisodeListModal(record.node.id)"
          ></a-button>
        </a-tooltip>
        <a-tooltip title="Sửa">
          <a-button
            type="link"
            icon="edit"
            size="small"
            class="mr-1"
            @click="onOpenEditDrawer(record.node.id)"
          ></a-button>
        </a-tooltip>
        <a-popconfirm
          title="Chắn chắn xoá?"
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
    <div class="row">
      <div class="col-lg-12 text-right mt-3">
        <pagination routePath="podcast" :options="pagination" />
      </div>
    </div>
    <podcast-edit />
    <episode-list-modal></episode-list-modal>
    <apple></apple>
  </a-layout-content>
</template>

<script lang="ts">
import { Vue, Component, Watch } from "vue-property-decorator";
import { bus, getVariables } from "@/helpers/utils";
import Pagination from "@/components/LayoutComponents/Pagination/index.vue";
import EpisodeAddModal from "@/components/Podcast/Episode/add.vue";
import EpisodeListModal from "@/components/Podcast/Episode/index.vue";
import Apple from "@/components/Podcast/ImportLink/Apple/index.vue";
import {
  GET_PODCASTS,
  CREATE_PODCAST,
  DELETE_PODCAST
} from "@/graphql/podcasts";
import PodcastAdd from "@/components/Podcast/Add/index.vue";
import PodcastEdit from "@/components/Podcast/Edit/index.vue";

@Component({
  name: "podcast-page",
  components: {
    Pagination,
    EpisodeAddModal,
    EpisodeListModal,
    Apple,
    PodcastAdd,
    PodcastEdit
  },
  apollo: {
    podcastsGraph: {
      query: GET_PODCASTS,
      variables() {
        return {
          first: this.pagination.pageSize,
          last: this.pagination.pageSize,
          sort: this.sort
        };
      },
      update(data) {
        return data.podcastList;
      },
      result({ data }) {
        this.pagination.total = data.podcastList.totalCount;
      },
      skip() {
        return this.skipQuery;
      },
      error(error) {
        this.$notification.error({
          message: "Fail to fetch podcastList!",
          description: error.toString(),
          duration: 5
        });
      }
    }
  }
})
export default class PodcastPage extends Vue {
  @Watch("$route") _routeChange() {
    this.init();
  }
  mediaUri: any = process.env.VUE_APP_MEDIA_URI;
  sort: any = ["ID_ASC"];
  // graphQL
  podcastsGraph: any = {
    edges: []
  };
  skipQuery: boolean = true;
  // pagination
  pagination: any = {
    size: "small",
    current: 1,
    total: 0,
    pageSize: 30,
    showQuickJumper: true
  };
  // data table
  columns: any = [
    {
      title: "#",
      dataIndex: "node.id",
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
      title: "Email liên hệ",
      dataIndex: "node.contactEmail",
      scopedSlots: {
        customRender: "_contactEmail"
      }
    },
    {
      title: "Website URL",
      dataIndex: "node.websiteUrl",
      scopedSlots: {
        customRender: "_websiteUrl"
      }
    },
    {
      title: "Copyright",
      dataIndex: "node.copyright",
      scopedSlots: {
        customRender: "_copyright"
      }
    },
    {
      title: "Trạng thái",
      width: "6%",
      dataIndex: "node.status",
      scopedSlots: {
        customRender: "_status"
      }
    },
    {
      width: "10%",
      scopedSlots: {
        customRender: "_actions"
      }
    }
  ];

  async onDelete(podcastId) {
    try {
      const res = await this.$apollo.mutate({
        mutation: DELETE_PODCAST,
        variables: {
          podcastId: podcastId
        }
      });

      if (res && res.data.deleted !== null) {
        this.$notification.success({
          message: "Xoá podcast thành công!",
          description: podcastId,
          duration: 2
        });

        this.$apollo.queries.podcastsGraph.skip = false;
        await this.$apollo.queries.podcastsGraph.refetch();
      }
    } catch (error) {
      this.$notification.error({
        message: "Lỗi trong quá trifnh xoá podcast!",
        description: error.toString(),
        duration: 5
      });
      return;
    }
  }

  async init() {
    const { page } = this.$route.query;
    const currentPage: any = typeof page !== "undefined" ? page : 1;
    const variables: any = getVariables(this.pagination, currentPage);

    this.$apollo.queries.podcastsGraph.skip = false;
    await this.$apollo.queries.podcastsGraph.refetch(variables);
  }

  created() {
    this.init();
    bus.$on("podcast:refresh", async () => {
      this.$apollo.queries.podcastsGraph.skip = false;
      await this.$apollo.queries.podcastsGraph.refetch();
    });
  }

  onOpenEpisodeAddModal(podcastId) {
    bus.$emit("episode:showAddModal", podcastId);
  }

  onOpenEpisodeListModal(podcastId) {
    bus.$emit("episode:showListModal", podcastId);
  }

  onOpenEditDrawer(podcastId) {
    bus.$emit("podcast:showEdit", podcastId);
  }

  onOpenImportFromAppleModal() {
    bus.$emit("podcast:showImportFromAppleModal");
  }
}
</script>

<style lang="scss" module scoped>
@import "./index.module.scss";
</style>
