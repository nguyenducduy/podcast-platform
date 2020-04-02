<template>
  <a-layout-content class="lg">
    <div class="utils__title mb-3">
      <strong class="text-uppercase font-size-16">Danh sách ({{ pagination.total }})</strong>
      <!-- <a-button type="primary" icon="plus" class="float-right mr-1" @click="onOpenAddModal()">Thêm</a-button> -->
      <common-upload />
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
      <p slot="_size" slot-scope="value">{{ value | fileSizeFormat }}</p>
      <p slot="_duration" slot-scope="value">{{ value | numeralFormat("00:00") }}</p>
      <p slot="_gcsId" slot-scope="value">{{ value }}</p>
      <p slot="_createdAt" slot-scope="value">{{ value | moment("Do MMMM YYYY") }}</p>
      <template slot="_name" slot-scope="record">
        <editable-cell
          :text="record.node.name"
          @change="onCellChange(record.node.id, 'name', $event)"
        />
      </template>
      <a-tag slot="_type" slot-scope="record" :color="record.node.type.color">
        {{
        record.node.type.text
        }}
      </a-tag>
      <a-tag
        slot="_is_common"
        slot-scope="record"
        :color="record.node.isCommon.color"
      >{{ record.node.isCommon.text }}</a-tag>
      <span slot="_actions" slot-scope="record">
        <inline-player :url="`${mediaUri}/${record.node.path}`" />
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
        <pagination routePath="admin/filedrive" :options="pagination" />
      </div>
    </div>
  </a-layout-content>
</template>

<script lang="ts">
import { Vue, Component, Watch } from "vue-property-decorator";
import { bus, getVariables } from "@/helpers/utils";
import InlinePlayer from "@/components/InlinePlayer/index.vue";
import Pagination from "@/components/LayoutComponents/Pagination/index.vue";
import {
  GET_ALL_FILEDRIVE,
  EDIT_FIELD,
  DELETE_FILEDRIVE
} from "@/graphql/filedrives";
import CommonUpload from "@/components/Filedrive/CommonUpload/index.vue";
import EditableCell from "@/components/EditableCell/index.vue";

@Component({
  name: "filedrive-page",
  components: {
    Pagination,
    InlinePlayer,
    CommonUpload,
    EditableCell
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
        title: "Is Common",
        width: "10%",
        key: "isCommon",
        // filters: this.usersGraph.groupList,
        scopedSlots: {
          customRender: "_is_common"
        }
      },
      {
        title: "Dung lượng",
        dataIndex: "node.size",
        width: "8%",
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
        title: "GCS ID",
        dataIndex: "node.gcsId",
        scopedSlots: {
          customRender: "_gcsId"
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

  async onCellChange(id, dataIndex, value) {
    try {
      const response = await this.$apollo.mutate({
        mutation: EDIT_FIELD,
        variables: {
          id: id,
          dataIndex: dataIndex,
          value: value
        }
      });

      if (response && response.data.filedriveEditField !== null) {
        this.$notification.success({
          message: `Cập nhật field "${dataIndex}" với giá trị "${value}"`,
          description: "",
          duration: 2
        });
      }
    } catch (error) {
      this.$notification.error({
        message: "Lỗi trong quá trình cập nhật!",
        description: error.toString(),
        duration: 5
      });
    }
  }

  async onDelete(id) {
    try {
      const res = await this.$apollo.mutate({
        mutation: DELETE_FILEDRIVE,
        variables: {
          filedriveId: id
        }
      });

      if (res && res.data.deleted !== null) {
        this.$notification.success({
          message: "Delete filedrive success!",
          description: id,
          duration: 2
        });

        this.$apollo.queries.filedrivesGraph.skip = false;
        await this.$apollo.queries.filedrivesGraph.refetch();
      }
    } catch (error) {
      this.$notification.error({
        message: "Delete filedrive failed!",
        description: error.toString(),
        duration: 5
      });
      return;
    }
  }

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
