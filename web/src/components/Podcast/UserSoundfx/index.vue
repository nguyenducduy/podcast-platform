<template>
  <div>
    <podcast-upload />
    <a-table
      class="soundfx"
      :dataSource="filedrivesGraph.edges"
      :columns="columns"
      :pagination="pagination"
      size="small"
      :rowKey="record => record.node.id"
      :loading="$apollo.loading"
      @change="onPageChange"
    >
      <template slot="__name_slot" slot-scope="record" :className="$style.soundfx">
        <editable-cell
          size="small"
          :text="record.node.name"
          @change="onCellChange(record.node.id, 'name', $event)"
        />
        <span class="duration ml-2">
          {{
          record.node.duration | numeralFormat("00:00")
          }}
        </span>
      </template>
      <a-tag
        slot="__type_slot"
        slot-scope="record"
        :color="record.node.type.color"
        style="font-size: 10px;"
      >{{ record.node.type.text }}</a-tag>
      <template slot="__actions_slot" slot-scope="record">
        <inline-player :url="`${mediaUri}/${record.node.path}`" />
        <a-popover placement="topLeft">
          <span slot="title">Merge with Crossfade Duration：{{ crossfadeDuration }}</span>
          <template slot="content">
            <a-input-number :min="1" v-model="crossfadeDuration" size="small" />
            <a-button
              type="primary"
              size="small"
              class="ml-2"
              :disabled="lock"
              @click="appendTo(record.node)"
            >Merge</a-button>
          </template>
          <a-button type="link" icon="arrow-right" :disabled="lock"></a-button>
        </a-popover>
        <a-tooltip title="Mix">
          <a-button type="link" icon="experiment" :disabled="lock" @click="onMixTo(record.node)"></a-button>
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
      </template>
    </a-table>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus } from "@/helpers/utils";
import {
  GET_USER_FILEDRIVE,
  EDIT_FIELD,
  DELETE_USER_FILEDRIVE
} from "@/graphql/filedrives";
import PodcastUpload from "@/components/Podcast/Upload/index.vue";
import EditableCell from "@/components/EditableCell/index.vue";
import InlinePlayer from "@/components/InlinePlayer/index.vue";

@Component({
  name: "user-soundfx",
  components: {
    PodcastUpload,
    EditableCell,
    InlinePlayer
  },
  apollo: {
    filedrivesGraph: {
      query: GET_USER_FILEDRIVE,
      variables() {
        return {
          first: this.pagination.pageSize,
          last: this.pagination.pageSize
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
          message: "Fail to fetch userFiledriveList!",
          description: error.toString(),
          duration: 5
        });
        return;
      }
    }
  }
})
export default class UserSoundfx extends Vue {
  mediaUri: any = process.env.VUE_APP_MEDIA_URI;

  // graphQL
  filedrivesGraph: any = {
    edges: []
  };
  skipQuery: boolean = true;
  // pagination
  pagination: any = {
    total: 0,
    pageSize: 10,
    showTotal: total => `Total ${total}`,
    hideOnSinglePage: true
  };
  // data table
  columns: any = [
    {
      title: "",
      scopedSlots: {
        customRender: "__name_slot"
      }
    },
    {
      title: "",
      width: "3%",
      scopedSlots: {
        customRender: "__type_slot"
      }
    },
    {
      title: "",
      width: "35%",
      scopedSlots: {
        customRender: "__actions_slot"
      }
    }
  ];

  crossfadeDuration: number = 2;
  sessionId: string = "";
  lock: boolean = false;
  mainlineTrack: any = null;

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

  onMixTo(fromTrack) {
    bus.$emit("mixtool:show", fromTrack, this.mainlineTrack, this.sessionId);
  }

  async onPageChange(pagination) {
    const totalPages = pagination.total / this.pagination.pageSize;

    await this.$apollo.queries.filedrivesGraph.fetchMore({
      variables: {
        first: this.pagination.pageSize * pagination.current,
        last:
          pagination.current > totalPages
            ? pagination.total % this.pagination.pageSize
            : this.pagination.pageSize
      },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        return {
          filedriveList: fetchMoreResult.filedriveList
        };
      }
    });
  }

  appendTo(track) {
    bus.$emit("composer:append", track, this.crossfadeDuration);
  }

  async onDelete(filedriveId) {
    try {
      const res = await this.$apollo.mutate({
        mutation: DELETE_USER_FILEDRIVE,
        variables: {
          filedriveId: filedriveId
        }
      });

      if (res && res.data.deleted !== null) {
        this.$notification.success({
          message: "Filedrive",
          description: `Xoá filedrive ${filedriveId} thành công`
        });

        this.$apollo.queries.filedrivesGraph.skip = false;
        await this.$apollo.queries.filedrivesGraph.refetch();
      }
    } catch (error) {
      this.$notification.error({
        message: "Lỗi trong quá trình xoá filedrive!",
        description: error.toString()
      });
    }
  }

  mounted() {
    bus.$on("soundfx:lockAppend", () => {
      this.lock = true;
    });
    bus.$on("soundfx:unLockAppend", () => {
      this.lock = false;
    });
    bus.$on("soundfx:initMainTrack", revision => {
      this.mainlineTrack = revision.mixedFile;
    });
    bus.$on("upload:success", async () => {
      this.$apollo.queries.filedrivesGraph.skip = false;
      await this.$apollo.queries.filedrivesGraph.refetch();
    });
    bus.$on("composer:sessionSelected", async data => {
      this.sessionId = data["sessionId"];
    });
    bus.$on("soundfx:updateSessionId", sessionId => {
      this.sessionId = sessionId;
    });
    bus.$on("userSoundfx:refresh", async () => {
      this.$apollo.queries.filedrivesGraph.skip = false;
      await this.$apollo.queries.filedrivesGraph.refetch();
    });
  }

  async created() {
    this.$apollo.queries.filedrivesGraph.skip = false;
    await this.$apollo.queries.filedrivesGraph.refetch();
  }
}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>

<style lang="scss">
.soundfx {
  td:first-child {
    word-break: break-all;
  }
  td {
    .duration {
      font-size: 11px;
      color: #aaa;
    }
    font-size: 12px;
    padding: 3px 3px !important;
  }
}
</style>
