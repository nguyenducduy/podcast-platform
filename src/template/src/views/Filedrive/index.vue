<template>
  <a-layout-content class="lg">
    <div class="utils__title mb-3">
      <strong class="text-uppercase font-size-16">Danh sách ({{ pagination.total }})</strong>
      <a-button type="primary" icon="plus" class="float-right mr-1" @click="onOpenAddModal()">Thêm</a-button>
    </div>
    <a-table
      :dataSource="filedrivesGraph.edges"
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
      <p slot="_size" slot-scope="value">{{ value }}</p>
      <p slot="_duration" slot-scope="value">{{ value | numeralFormat("00:00") }}</p>
      <p slot="_createdAt" slot-scope="value">{{ value | moment("dddd, Do MMMM YYYY") }}</p>
      <!-- <a slot="_cover" slot-scope="record" :class="$style.thumbnail">
        <img :src="`${mediaUri}/${record.node.avatar}`" />
      </a>-->
      <p slot="_name" slot-scope="value">{{ value }}</p>
      <a-tag slot="_type" slot-scope="record" :color="record.node.type.color">
        {{
        record.node.type.text
        }}
      </a-tag>
      <span slot="_actions" slot-scope="record">
        <inline-player :url="`${mediaUri}/${record.node.path}`" />
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
        <pagination routePath="filedrive" :options="pagination" />
      </div>
    </div>

    <!-- <podcast-add-modal></podcast-add-modal>
    <podcast-edit-modal></podcast-edit-modal>
    <episode-list-modal></episode-list-modal>-->
  </a-layout-content>
</template>

<script lang="ts">
import { Vue, Component, Watch } from "vue-property-decorator";
import { bus, getVariables } from "@/helpers/utils";
// import PodcastAddModal from "@/components/Podcast/AddModal/index.vue";
// import PodcastEditModal from "@/components/Podcast/EditModal/index.vue";
import InlinePlayer from "@/components/InlinePlayer/index.vue";
import Pagination from "@/components/LayoutComponents/Pagination/index.vue";
import { GET_ALL_FILEDRIVE } from "@/graphql/filedrives";

@Component({
  name: "filedrive-page",
  components: {
    Pagination,
    InlinePlayer
  },
  apollo: {
    filedrivesGraph: {
      query: GET_ALL_FILEDRIVE,
      variables() {
        return {
          first: this.pagination.pageSize,
          last: this.pagination.pageSize
          // sort: ["ID_DESC"]
        };
      },
      update(data) {
        return data.filedriveList;
      },
      result({ data }) {
        this.pagination.total = data.filedriveList.totalCount;
      },
      skip() {
        return this.skipQuery;
      },
      error(error) {
        this.$notification.error({
          message: "Fail to fetch filedriveList!",
          description: error.toString(),
          duration: 5
        });
      }
    }
  }
})
export default class FiledrivePage extends Vue {
  @Watch("$route") _routeChange() {
    this.init();
  }
  mediaUri: any = process.env.VUE_APP_MEDIA_URI;
  // graphQL
  filedrivesGraph: any = {
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

  get columns() {
    const columns: any = [
      {
        title: "#",
        dataIndex: "node.id",
        scopedSlots: {
          customRender: "_id"
        }
      },
      {
        title: "Tên file",
        dataIndex: "node.name",
        scopedSlots: {
          customRender: "_name"
        }
      },
      {
        title: "Loại",
        width: "10%",
        key: "type",
        // filters: this.usersGraph.groupList,
        scopedSlots: {
          customRender: "_type"
        }
      },
      {
        title: "Dung lượng",
        dataIndex: "node.size",
        scopedSlots: {
          customRender: "_size"
        }
      },
      {
        title: "Độ dài",
        dataIndex: "node.duration",
        scopedSlots: {
          customRender: "_duration"
        }
      },
      {
        title: "Ngày tạo",
        dataIndex: "node.createdAt",
        scopedSlots: {
          customRender: "_createdAt"
        }
      },
      {
        width: "10%",
        scopedSlots: {
          customRender: "_actions"
        }
      }
    ];
    return columns;
  }

  async onOpenAddModal() {}

  async onOpenEditModal(id) {}

  async onDelete(id) {}

  created() {
    this.init();
  }

  async init() {
    const { page } = this.$route.query;
    const currentPage: any = typeof page !== "undefined" ? page : 1;
    const variables: any = getVariables(this.pagination, currentPage);
    this.$apollo.queries.filedrivesGraph.skip = false;
    await this.$apollo.queries.filedrivesGraph.refetch(variables);
  }
}
</script>
