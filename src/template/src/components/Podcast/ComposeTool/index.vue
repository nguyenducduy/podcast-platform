<template>
  <div>
    <div class="pb-3 justify-start">
      <h1 class="text-xl pb-1">
        <a-tag color="#87d068">{{ sessionId }} #{{ version }}</a-tag>
      </h1>
    </div>
    <hr class="mb-3" />
    <div v-if="revisionsGraph.edges.length === 0" class="flex justify-center">
      <a-empty />
    </div>
    <div v-else class="flex items-start">
      <a-spin tip="Đang xử lý..." :spinning="spinning">
        <div class="spin-content">
          <draggable
            tag="ul"
            class="w-full max-w compose-list"
            :list="tracks"
            :animation="200"
            ghost-class="moving-card"
            filter=".action-button"
            style="text-align: center"
            :sort="dragEnable"
            @change="onChange"
          >
            <li
              v-for="(track, idx) in tracks"
              :key="track.key"
              class="p-2 pl-4 mb-3 flex justify-between items-center cursor-move"
            >
              <span :class="$style.composeTitle">{{ track.label }}</span>
              <div style="float: right;margin-right: 10px;clear: both;">
                <!-- <a-tag color="#2db7f5">#{{ track.fdId }}</a-tag> -->
                <!-- <small v-if="track.type == 'mix'"
                  >{{ track.start }} -> {{ track.end }}</small
                >
                &nbsp;-->
                <!-- <a-button
                  type="link"
                  icon="sound"
                  class="focus:outline-none focus:shadow-outline text-teal-500 hover:text-teal-600"
                ></a-button>-->
                <a-tag :color="track.type == 'crossfade' ? 'cyan' : 'purple'">{{
                  track.type
                }}</a-tag>
                <a-button
                  @click="onRemove(idx)"
                  type="link"
                  icon="delete"
                  class="focus:outline-none focus:shadow-outline text-red-500 hover:text-red-600"
                ></a-button>
              </div>
            </li>
          </draggable>
        </div>
      </a-spin>
      <mix-tool />
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import MixTool from "@/components/Podcast/MixTool/index.vue";
import draggable from "vuedraggable";
import { bus, randomID } from "@/helpers/utils";
import {
  GET_REVISIONS,
  CREATE_REVISION,
  DETACH_REVISION,
  CHANGE_FILE_ORDER_IN_REVISION
} from "@/graphql/revisions";

@Component({
  name: "compose-tool",
  components: {
    draggable,
    MixTool
  },
  apollo: {
    revisionsGraph: {
      query: GET_REVISIONS,
      variables() {
        return {
          first: this.pagination.itemsPerPage,
          last: this.pagination.pageSize
        };
      },
      update(data) {
        return data.revisionList;
      },
      result({ data }) {
        this.pagination.total = data.revisionList.totalCount;
      },
      skip() {
        return this.skipQuery;
      },
      error(error) {
        this.$notification.error({
          message: "Fail to fetch revisionsGraph!",
          description: error.toString(),
          duration: 5
        });
        return;
      }
    }
  }
})
export default class ComposeTool extends Vue {
  tracks: any = [];
  crossfadeDuration: Number = 2;
  revisionsGraph: any = {
    edges: []
  };
  skipQuery: boolean = true;
  pagination: any = {
    total: 0,
    pageSize: 100
  };
  spinning: boolean = false;
  sessionId: string = "";
  version: number = 0;
  dragEnable: boolean = true;

  async onChange(evt) {
    if (this.dragEnable === false) {
      this.$notification.error({
        message: "Không thể thay đổi thứ tự vì Session ID này đã đc MIX",
        description: "",
        duration: 10
      });
      return;
    }

    let arrChanged = "";
    this.tracks.map(track => {
      arrChanged += track.key + ",";
    });

    try {
      this.spinning = true;

      const res = await this.$apollo.mutate({
        mutation: CHANGE_FILE_ORDER_IN_REVISION,
        variables: {
          newTracksOrder: arrChanged.slice(0, -1),
          sessionId: this.sessionId,
          version: this.version
        }
      });

      await this.$apollo.queries.revisionsGraph.refetch({
        sessionId: this.sessionId,
        version: res.data.changeFileOrderInRevision.revision.version
      });

      this.version = res.data.changeFileOrderInRevision.revision.version;
      this._loadRevision();
      this.spinning = false;
      bus.$emit("history:refresh");
    } catch (error) {
      this.spinning = false;

      this.$notification.error({
        message: "Fail to change order in file revision!",
        description: error.toString(),
        duration: 5
      });
      return;
    }
  }

  async onRemove(idx) {
    try {
      this.spinning = true;

      const res = await this.$apollo.mutate({
        mutation: DETACH_REVISION,
        variables: {
          sessionId: this.sessionId,
          version: this.version,
          detachIndex: idx
        }
      });

      await this.$apollo.queries.revisionsGraph.refetch({
        sessionId: this.sessionId,
        version: res.data.detachRevision.revision.version
      });

      this.version = res.data.detachRevision.revision.version;
      this._loadRevision();
      this.spinning = false;
      bus.$emit("history:refresh");
    } catch (error) {
      this.$notification.error({
        message: "Fail to detach track from composer!",
        description: error.toString(),
        duration: 5
      });
      return;
    }
  }

  created() {
    bus.$on("composer:append", async track => {
      bus.$emit("soundfx:lockAppend");

      this.spinning = true;

      try {
        const res = await this.$apollo.mutate({
          mutation: CREATE_REVISION,
          variables: {
            sessionId: this.sessionId,
            content: JSON.stringify({
              action: "crossfade",
              fdId: parseInt(track.id),
              crossfadeDuration: this.crossfadeDuration
            })
          }
        });

        await this.$apollo.queries.revisionsGraph.refetch({
          sessionId: this.sessionId,
          version: res.data.createRevision.revision.version
        });

        this.version = res.data.createRevision.revision.version;
        this._loadRevision();
        this.spinning = false;
      } catch (error) {
        this.$notification.error({
          message: "Fail to Create revision!",
          description: error.toString(),
          duration: 5
        });
        return;
      }

      bus.$emit("soundfx:unLockAppend");
      bus.$emit("soundfx:updateSessionId", this.sessionId);
    });

    bus.$on("composer:mixSuccess", async version => {
      await this.$apollo.queries.revisionsGraph.refetch({
        sessionId: this.sessionId,
        version: version
      });
      this.version = version;
      this._loadRevision();
    });

    bus.$on("composer:sessionSelected", async data => {
      this.sessionId = data["sessionId"];
      this.version = data["version"];

      await this.$apollo.queries.revisionsGraph.refetch({
        sessionId: data["sessionId"],
        version: data["version"]
      });
      this._loadRevision();
    });
  }

  async mounted() {
    this.sessionId = randomID();
    this.$apollo.queries.revisionsGraph.skip = false;
  }

  _loadRevision() {
    this.dragEnable = true;
    this.tracks = [];

    if (this.revisionsGraph.edges.length > 0) {
      let revisionData = this.revisionsGraph.edges[0].node;

      JSON.parse(revisionData.content).forEach(track => {
        let count = this.tracks.length;

        if (track.type == "mix") {
          this.dragEnable = false;
        }

        this.tracks.push({
          key: count++,
          ...track
        });
      });

      bus.$emit(
        "visual:render",
        revisionData.mixedFile,
        JSON.parse(revisionData.content)
      );
      bus.$emit("soundfx:initMainTrack", revisionData);
    }
  }
}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
