<template>
  <div>
    <h3 class="mt-4">FILE CHUNG</h3>
    <a-table
      class="soundfx"
      :dataSource="filedrivesGraph.edges"
      :columns="columns"
      :pagination="pagination"
      size="small"
      :rowKey="record => record.cursor"
      :loading="$apollo.loading"
      @change="onPageChange"
    >
      <template slot="__name_slot" slot-scope="record" :className="$style.soundfx">
        {{ record.node.name }}
        <span
          class="duration"
        >{{ record.node.duration | numeralFormat("00:00") }}</span>
      </template>
      <a-tag
        slot="__type_slot"
        slot-scope="record"
        :color="record.node.type.color"
      >{{ record.node.type.text }}</a-tag>
      <template slot="__actions_slot" slot-scope="record">
        <inline-player :url="`${mediaUri}/${record.node.path}`" />
        <a-popover placement="topLeft">
          <span slot="title">Merge with Crossfade Duration：{{crossfadeDuration}}</span>
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
        <!-- <a-tooltip title="Trim silence">
          <a-button type="link" icon="scissor" :disabled="lock" @click="onTrimSilence(record.node)"></a-button>
        </a-tooltip>-->
      </template>
    </a-table>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus } from "@/helpers/utils";
import { GET_COMMON_FILEDRIVE } from "@/graphql/filedrives";
import InlinePlayer from "@/components/InlinePlayer/index.vue";

@Component({
  name: "soundfx",
  components: {
    InlinePlayer
  },
  apollo: {
    filedrivesGraph: {
      query: GET_COMMON_FILEDRIVE,
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
export default class Soundfx extends Vue {
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
    showQuickJumper: true,
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
      width: "25%",
      scopedSlots: {
        customRender: "__actions_slot"
      }
    }
  ];

  crossfadeDuration: number = 2;
  sessionId: string = "";
  lock: boolean = false;
  mainlineTrack: any = null;

  onMixTo(fromTrack) {
    bus.$emit("mixtool:show", fromTrack, this.mainlineTrack, this.sessionId);
  }

  onTrimSilence() {
    console.log("trim action");
  }

  onPlayPause(cursor) {
    const newData = [...this.filedrivesGraph.edges];

    const track = newData.filter(item => cursor === item.cursor)[0];
    if (track) {
      if (track.hasOwnProperty("playing")) {
        if (track.playing === true) {
          track.player.pause();
          track.playing = false;
        } else {
          track.player.play();
          track.playing = true;
        }

        this.filedrivesGraph.edges = newData;
        return;
      }
      const mySound = new Audio(`${this.mediaUri}/${track.node.path}`);
      track.playing = true;
      track.player = mySound;
      track.player.play();
      this.filedrivesGraph.edges = newData;

      const self = this;
      track.player.addEventListener("ended", function() {
        console.log("audio ended:" + cursor);
      });
    }
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
      color: #ccc;
    }
    font-size: 12px;
    padding: 3px 3px !important;
  }
}
</style>
