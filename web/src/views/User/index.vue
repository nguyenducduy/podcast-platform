<template>
  <a-layout-content class="lg">
    <div class="utils__title mb-3">
      <strong class="text-uppercase font-size-16"
        >Danh sách ({{ pagination.total }})</strong
      >
      <user-add-drawer />
    </div>
    <a-table
      :dataSource="usersGraph.edges"
      :columns="columns"
      :pagination="false"
      size="small"
      :rowKey="record => record.node.id"
      :loading="$apollo.loading"
    >
      <a slot="_id" slot-scope="value" class="utils__link--underlined">{{
        value
      }}</a>
      <!-- <a slot="_cover" slot-scope="record" :class="$style.thumbnail">
        <img :src="`${mediaUri}/${record.node.avatar}`" />
      </a>-->
      <p slot="_name" slot-scope="value">{{ value }}</p>
      <a-tag
        slot="_group"
        slot-scope="record"
        :color="record.node.group.color"
        >{{ record.node.group.text }}</a-tag
      >
      <span slot="_actions" slot-scope="record">
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
        <pagination routePath="user" :options="pagination" />
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
import Pagination from "@/components/LayoutComponents/Pagination/index.vue";
import { GET_USERS } from "@/graphql/users";
import UserAddDrawer from "@/components/User/Add/index.vue";
// import gql from "graphql-tag";

@Component({
  name: "user-page",
  components: {
    Pagination,
    UserAddDrawer
    // PodcastAddModal,
    // PodcastEditModal,
    // EpisodeAddModal,
    // EpisodeListModal
  },
  apollo: {
    // $subscribe: {
    //   tags: {
    //     query: gql`subscription {
    //       countSeconds(upTo: 10)
    //     }`,
    //     result ({ data }) {
    //       console.log(data);
    //     },
    //   },
    // },
    usersGraph: {
      query: GET_USERS,
      variables() {
        return {
          first: this.pagination.pageSize,
          last: this.pagination.pageSize
          // sort: ["ID_DESC"]
        };
      },
      update(data) {
        return data.userList;
      },
      result({ data }) {
        this.pagination.total = data.userList.totalCount;
      },
      skip() {
        return this.skipQuery;
      },
      error(error) {
        this.$notification.error({
          message: "Fail to fetch userList!",
          description: error.toString(),
          duration: 5
        });
      }
    }
  }
})
export default class UserPage extends Vue {
  @Watch("$route") _routeChange() {
    this.init();
  }
  mediaUri: any = process.env.VUE_APP_MEDIA_URI;

  // graphQL
  usersGraph: any = {
    edges: []
  };

  // filters: any = {
  //   groupId: []
  // };
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
        scopedSlots: {
          customRender: "_cover"
        }
      },
      {
        title: "Tên",
        dataIndex: "node.fullName",
        scopedSlots: {
          customRender: "_name"
        }
      },
      {
        title: "Group",
        width: "10%",
        key: "group",
        // filters: this.usersGraph.groupList,
        scopedSlots: {
          customRender: "_group"
        }
      },
      {
        width: "8%",
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

  async created() {
    this.init();
  }

  async init() {
    const { page } = this.$route.query;
    const currentPage: any = typeof page !== "undefined" ? page : 1;
    const variables: any = getVariables(this.pagination, currentPage);

    this.$apollo.queries.usersGraph.skip = false;
    await this.$apollo.queries.usersGraph.refetch(variables);
  }
}
</script>

<style lang="scss" module scoped>
@import "./index.module.scss";
</style>
