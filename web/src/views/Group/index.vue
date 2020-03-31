<template>
  <a-layout-content class="lg">
    <div class="utils__title mb-3">
      <strong class="text-uppercase font-size-16"
        >Danh sách ({{ pagination.total }})</strong
      >
      <group-add-drawer />
    </div>
    <a-table
      :dataSource="groupsGraph.edges"
      :columns="columns"
      :pagination="false"
      size="small"
      :rowKey="record => record.node.id"
      :loading="$apollo.loading"
    >
      <a slot="_id" slot-scope="value" class="utils__link--underlined">
        {{ value }}
      </a>
      <p slot="_name" slot-scope="value">{{ value }}</p>
      <a-tag
        slot="_screenName"
        slot-scope="record"
        :color="record.node.color"
        >{{ record.node.screenName }}</a-tag
      >

      <span slot="_actions" slot-scope="record">
        <a-button
          type="dashed"
          size="small"
          class="mr-1"
          @click="onOpenGrantDrawer(record.node.id)"
          >Gán quyền</a-button
        >
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
        <pagination routePath="admin/group" :options="pagination" />
      </div>
    </div>
    <group-edit-drawer />
    <permission-grant-drawer />
  </a-layout-content>
</template>

<script lang="ts">
import { Vue, Component, Watch } from "vue-property-decorator";
import { bus, getVariables } from "@/helpers/utils";
import Pagination from "@/components/LayoutComponents/Pagination/index.vue";
import { GET_GROUPS, DELETE_GROUP } from "@/graphql/groups";
import GroupAddDrawer from "@/components/Group/Add/index.vue";
import GroupEditDrawer from "@/components/Group/Edit/index.vue";
import PermissionGrantDrawer from "@/components/Permission/Grant/index.vue";

@Component({
  name: "group-page",
  components: {
    Pagination,
    GroupAddDrawer,
    GroupEditDrawer,
    PermissionGrantDrawer
  },
  apollo: {
    groupsGraph: {
      query: GET_GROUPS,
      variables() {
        return {
          first: this.pagination.pageSize,
          last: this.pagination.pageSize,
          sort: this.sort
        };
      },
      update(data) {
        return data.groupList;
      },
      result({ data }) {
        this.pagination.total = data.groupList.totalCount;
      },
      skip() {
        return this.skipQuery;
      },
      error(error) {
        this.$notification.error({
          message: "Fail to fetch groupList!",
          description: error.toString(),
          duration: 5
        });
      }
    }
  }
})
export default class GroupPage extends Vue {
  @Watch("$route") _routeChange() {
    this.init();
  }

  // graphQL
  groupsGraph: any = {
    edges: []
  };
  skipQuery: boolean = true;

  // filters: any = {
  //   groupId: []
  // };

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
        title: "Tên (giá trị)",
        dataIndex: "node.name",
        scopedSlots: {
          customRender: "_name"
        }
      },
      {
        title: "Tên (hiển thị)",
        scopedSlots: {
          customRender: "_screenName"
        }
      },
      {
        width: "16%",
        scopedSlots: {
          customRender: "_actions"
        }
      }
    ];

    return columns;
  }

  async onDelete(id) {
    try {
      const res = await this.$apollo.mutate({
        mutation: DELETE_GROUP,
        variables: {
          id: id
        }
      });

      if (res && res.data.deleted !== null) {
        this.$notification.success({
          message: "Xoá group thành công!",
          description: id,
          duration: 5
        });

        this.$apollo.queries.groupsGraph.skip = false;
        await this.$apollo.queries.groupsGraph.refetch();
      }
    } catch (error) {
      this.$notification.error({
        message: "Lỗi trong quá trình xoá group!",
        description: error.toString(),
        duration: 5
      });
    }
  }

  onOpenEditDrawer(id) {
    bus.$emit("group:showEdit", id);
  }

  onOpenGrantDrawer(id) {
    bus.$emit("permission:showGrant", id);
  }

  async created() {
    this.init();
    bus.$on("group:refresh", async () => {
      this.$apollo.queries.groupsGraph.skip = false;
      await this.$apollo.queries.groupsGraph.refetch();
    });
  }

  async init() {
    const { page } = this.$route.query;
    const currentPage: any = typeof page !== "undefined" ? page : 1;
    const variables: any = getVariables(this.pagination, currentPage);

    this.$apollo.queries.groupsGraph.skip = false;
    await this.$apollo.queries.groupsGraph.refetch(variables);
  }
}
</script>
