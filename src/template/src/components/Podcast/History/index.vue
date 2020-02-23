<template>
  <div>
    <div class="p-3 mb-3 justify-start">
      <h3>Lịch sử chỉnh sửa</h3>
      <small>Nhấn vào Session ID để tiếp tục</small>
    </div>
    <div v-if="historiesGraph.edges.length === 0" class="flex justify-center">
      <a-empty />
    </div>
    <div v-else class>
      <a-timeline>
        <a-timeline-item v-for="(item, idx) in historiesGraph.edges" :key="idx">
          <div class="row">
            <div class="col-lg-10">
              <a-button
                size="small"
                type="primary"
                @click="onSessionSelect(item.node.sessionId, item.node.version)"
                >{{ item.node.sessionId }} #{{ item.node.version }}</a-button
              >
              {{ item.node.createdAt | moment("Do MMMM YYYY, h:mm a") }}
            </div>
            <!-- <div class="col-lg-2">
              <a-button size="small" icon="undo" type="link" style="font-size: 11px"></a-button
              >
            </div>-->
          </div>
        </a-timeline-item>
      </a-timeline>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus } from "@/helpers/utils";
import { GET_HISTORIES } from "@/graphql/revisions";

@Component({
  name: "podcast-history",
  apollo: {
    historiesGraph: {
      query: GET_HISTORIES,
      variables() {
        return {
          first: this.pagination.pageSize,
          last: this.pagination.pageSize
        };
      },
      update(data) {
        return data.viewer.historyList;
      },
      result({ data }) {
        this.pagination.total = data.viewer.historyList.totalCount;
      },
      skip() {
        return this.skipQuery;
      },
      error(error) {
        this.$notification.error({
          message: "Fail to fetch historiesGraph!",
          description: error.toString(),
          duration: 5
        });
        return;
      }
    }
  }
})
export default class PodcastHistory extends Vue {
  historiesGraph: any = {
    edges: []
  };
  skipQuery: boolean = true;
  pagination: any = {
    total: 0,
    pageSize: 100
  };

  onSessionSelect(sessionId, version) {
    bus.$emit("composer:sessionSelected", {
      sessionId: sessionId,
      version: version
    });
  }

  mounted() {
    bus.$on("soundfx:unLockAppend", async () => {
      await this.$apollo.queries.historiesGraph.refetch();
    });
    bus.$on("composer:mixSuccess", async () => {
      await this.$apollo.queries.historiesGraph.refetch();
    });
    bus.$on("history:refresh", async () => {
      await this.$apollo.queries.historiesGraph.refetch();
    });
  }

  async created() {
    this.$apollo.queries.historiesGraph.skip = false;
    await this.$apollo.queries.historiesGraph.refetch();
  }
}
</script>
