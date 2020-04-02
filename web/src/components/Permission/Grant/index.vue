<template>
  <div :style="{
      position: 'relative',
      float: 'right'
    }">
    <a-drawer
      :title="`Gán quyền cho nhóm #${group.id} ${group.screenName}`"
      placement="right"
      :visible="visible"
      :width="640"
      :closable="false"
      @close="onClose"
      :wrapStyle="{
        height: 'calc(100% - 108px)',
        overflow: 'auto',
        paddingBottom: '108px'
      }"
    >
      <div class="row">
        <div class="col-lg-12">
          <a-input-search
            placeholder="Search by query/mutation or description"
            @search="onSearch"
            class="mb-2"
          />

          <a-table
            class="mb-5"
            :pagination="{
              pageSize: 1000,
              hideOnSinglePage: true
            }"
            :rowSelection="{
              selectedRowKeys: selectedRowKeys,
              onChange: onSelectChange
            }"
            :dataSource="permissionList"
            :columns="columns"
            size="small"
            :rowKey="record => record.node.id"
            :loading="$apollo.loading"
          ></a-table>
        </div>
      </div>

      <div
        :style="{
          position: 'absolute',
          left: 0,
          bottom: 0,
          width: '100%',
          borderTop: '1px solid #e9e9e9',
          padding: '10px 16px',
          background: '#fff',
          textAlign: 'right'
        }"
      >
        <a-button type="danger" :style="{ marginRight: '8px' }" @click="onClose">Huỷ</a-button>
        <a-button
          type="primary"
          :style="{ marginRight: '8px' }"
          @click="onSubmit"
          :loading="loading"
        >Gán</a-button>
      </div>
    </a-drawer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { GET_PERMISSIONS } from "@/graphql/permissions";
import { GET_GROUP, GRANT_PERMISSION } from "@/graphql/groups";
import { bus } from "@/helpers/utils";
import _ from "lodash";

@Component({
  name: "permission-grant-drawer"
})
export default class PermissionGrant extends Vue {
  visible: boolean = false;
  form: any = {};
  loading: boolean = false;
  permissionList: any = [];

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

  selectedRowKeys: any = [];
  groupId: number = 0;
  group: any = {};

  get hasSelected() {
    return this.selectedRowKeys.length > 0;
  }

  onShow() {
    this.visible = true;
  }

  onClose() {
    this.visible = false;
  }

  onSelectChange(selectedRowKeys) {
    this.selectedRowKeys = selectedRowKeys;
  }

  onSearch(value) {
    console.log(value);
  }

  async onSubmit(e) {
    e.preventDefault();
    this.loading = true;

    try {
      const res = await this.$apollo.mutate({
        mutation: GRANT_PERMISSION,
        variables: {
          id: this.group.id,
          permissions: this.selectedRowKeys
        },
        // refetch to update apollo query cache (important)
        refetchQueries: [
          {
            query: GET_GROUP,
            variables: { id: this.group.id }
          }
        ]
      });

      if (res && res.data.granted !== null) {
        this.$notification.success({
          message: "Gán quyền",
          description: `Gán quyền cho nhóm "${this.group.screenName}" thành công`
        });
      }

      this.loading = false;
    } catch (error) {
      this.loading = false;

      this.$notification.error({
        message: "Lỗi trong quá trình gán quyền",
        description: error.toString()
      });
    }
  }

  async created() {
    bus.$on("permission:showGrant", async groupId => {
      this.loading = true;
      this.selectedRowKeys = [];
      this.groupId = groupId;
      this.visible = true;

      // get all permissions
      const res = await this.$apollo.query({
        query: GET_PERMISSIONS,
        variables: {
          first: 1000,
          last: 1000
        }
      });

      this.permissionList = res.data.permissionList.edges;

      // get info of selected group
      const res2 = await this.$apollo.query({
        query: GET_GROUP,
        variables: {
          id: groupId
        }
      });

      if (res2.data.group) {
        this.group = res2.data.group;
        const permissions = res2.data.group.permissions;

        permissions.map(perm => {
          this.selectedRowKeys.push(perm.id);
        });
      }

      this.loading = false;
    });
  }
}
</script>
