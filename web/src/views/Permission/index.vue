<template>
  <a-layout-content class="lg">
    <div class="utils__title mb-3">
      <strong class="text-uppercase font-size-16">Danh sách ({{ pagination.total }})</strong>
      <permission-add-drawer />
    </div>
    <a-table
      :dataSource="permissionsGraph.edges"
      :columns="columns"
      :pagination="false"
      size="small"
      :rowKey="record => record.node.id"
      :loading="$apollo.loading"
    >
      <a slot="_id" slot-scope="value" class="utils__link--underlined">{{ value }}</a>

      <span slot="_actions" slot-scope="record">
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
        <pagination routePath="admin/permission" :options="pagination" />
      </div>
    </div>
    <permission-edit-drawer />
  </a-layout-content>
</template>

<script lang="ts">
import { Vue, Component, Watch } from "vue-property-decorator";
import { bus, getVariables } from "@/helpers/utils";
import Pagination from "@/components/LayoutComponents/Pagination/index.vue";
import { GET_PERMISSIONS, DELETE_PERMISSION } from "@/graphql/permissions";
import PermissionAddDrawer from "@/components/Permission/Add/index.vue";
import PermissionEditDrawer from "@/components/Permission/Edit/index.vue";

@Component({
  name: "permission-page",
  components: {
    Pagination,
    PermissionAddDrawer,
    PermissionEditDrawer
  },
  apollo: {
    permissionsGraph: {
      query: GET_PERMISSIONS,
      variables() {
        return {
          first: this.pagination.pageSize,
          last: this.pagination.pageSize,
          sort: this.sort
        };
      },
      update(data) {
        return data.permissionList;
      },
      result({ data }) {
        this.pagination.total = data.permissionList.totalCount;
      },
      skip() {
        return this.skipQuery;
      },
      error(error) {
        this.$notification.error({
          message: "Fail to fetch permissionList!",
          description: error.toString(),
          duration: 5
        });
      }
    }
  }
})
export default class PermissionPage extends Vue {
  @Watch("$route") _routeChange() {
    this.init();
  }

  // graphQL
  permissionsGraph: any = {
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
        title: "Tên (Query/Mutation)",
        dataIndex: "node.name",
        scopedSlots: {
          customRender: "_name"
        }
      },
      {
        title: "Mô tả",
        dataIndex: "node.description",
        scopedSlots: {
          customRender: "_description"
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

  async onDelete(id) {
    try {
      const res = await this.$apollo.mutate({
        mutation: DELETE_PERMISSION,
        variables: {
          id: id
        },
        refetchQueries: [{ query: GET_PERMISSIONS }]
      });

      if (res && res.data.deleted !== null) {
        this.$notification.success({
          message: "Quyền",
          description: `Xoá quyền #${id} thành công`
        });

        this.$apollo.queries.permissionsGraph.skip = false;
        await this.$apollo.queries.permissionsGraph.refetch();
      }
    } catch (error) {
      this.$notification.error({
        message: "Lỗi trong quá trình xoá quyền!",
        description: error.toString()
      });
    }
  }

  onOpenEditDrawer(id) {
    bus.$emit("permission:showEdit", id);
  }

  async created() {
    this.init();
    bus.$on("permission:refresh", async () => {
      this.$apollo.queries.permissionsGraph.skip = false;
      await this.$apollo.queries.permissionsGraph.refetch();
    });
  }

  async init() {
    const { page } = this.$route.query;
    const currentPage: any = typeof page !== "undefined" ? page : 1;
    const variables: any = getVariables(this.pagination, currentPage);

    this.$apollo.queries.permissionsGraph.skip = false;
    await this.$apollo.queries.permissionsGraph.refetch(variables);
  }
}
</script>
