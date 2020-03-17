<template>
  <div>
    <a-button type="primary" @click="showDrawer">Chọn file cho Episode</a-button>
    <p class="mt-2" v-if="selectedFile !== null">{{ selectedFile.name }}</p>
    <a-drawer
      title="Danh sách file"
      placement="right"
      :closable="false"
      :visible="visible"
      :width="460"
      :wrapStyle="{height: 'calc(100% - 108px)',overflow: 'auto',paddingBottom: '108px'}"
    >
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
          {{ record.node.name }}
          <span
            class="duration ml-2"
          >{{ record.node.duration | numeralFormat("00:00") }}</span>
        </template>
        <a-tag
          slot="__type_slot"
          slot-scope="record"
          :color="record.node.type.color"
          style="font-size: 10px;"
        >{{ record.node.type.text }}</a-tag>
        <template slot="__actions_slot" slot-scope="record">
          <inline-player :url="`${mediaUri}/${record.node.path}`" />
          <a-button size="small" type="primary" @click="onChoose(record.node)">Chọn</a-button>
        </template>
      </a-table>
      <div
        :style="{
          position: 'absolute',
          left: 0,
          bottom: 0,
          width: '100%',
          borderTop: '1px solid #e9e9e9',
          padding: '10px 16px',
          background: '#fff',
          textAlign: 'right',
        }"
      >
        <a-button :style="{marginRight: '8px'}" @click="onClose">Đóng</a-button>
      </div>
    </a-drawer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus } from "@/helpers/utils";
import { GET_EPISODE_FILEDRIVE } from "@/graphql/filedrives";
import InlinePlayer from "@/components/InlinePlayer/index.vue";

@Component({
  name: "episode-file-list",
  components: {
    InlinePlayer
  },
  apollo: {
    filedrivesGraph: {
      query: GET_EPISODE_FILEDRIVE,
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
          message: "Fail to fetch filedriveList!",
          description: error.toString(),
          duration: 5
        });
        return;
      }
    }
  }
})
export default class EpisodeFileList extends Vue {
  mediaUri: any = process.env.VUE_APP_MEDIA_URI;
  visible: boolean = false;

  // graphQL
  filedrivesGraph: any = {
    edges: []
  };
  skipQuery: boolean = true;
  // pagination
  pagination: any = {
    total: 0,
    pageSize: 20,
    showTotal: total => `Total ${total}`,
    showQuickJumper: true,
    hideOnSinglePage: true
  };
  // data table
  columns: any = [
    {
      title: "Filename",
      scopedSlots: {
        customRender: "__name_slot"
      }
    },
    {
      title: "Loại",
      width: "3%",
      scopedSlots: {
        customRender: "__type_slot"
      }
    },
    {
      title: "",
      width: "25%",
      scopedSlots: {
        customRender: "__actions_slot"
      }
    }
  ];

  selectedFile: any = null;

  onChoose(file) {
    bus.$emit("episode:chooseFile", file.id, file.name);
    this.selectedFile = file;
    this.visible = false;
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

  async created() {
    bus.$on("episodefilelist:selected", file => {
      this.selectedFile = file;
    });

    this.$apollo.queries.filedrivesGraph.skip = false;
    await this.$apollo.queries.filedrivesGraph.refetch();
  }

  showDrawer() {
    this.visible = true;
  }

  onClose() {
    this.visible = false;
  }
}
</script>

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

