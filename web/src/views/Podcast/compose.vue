<template>
  <div class="row">
    <div class="col-lg-12 mb-3">
      <podcast-visual />
    </div>
    <div class="col-lg-4 bg-gray-100 rounded-lg">
      <recorder />
      <a-tabs tabPosition="top" class="mt-3">
        <a-tab-pane tab="File chung" key="1">
          <soundfx />
        </a-tab-pane>
        <a-tab-pane tab="File của bạn" key="2">
          <user-soundfx />
        </a-tab-pane>
      </a-tabs>
    </div>
    <div class="col-lg-8">
      <div class="row">
        <div class="col-lg-6">
          <compose-tool />
        </div>
        <div class="col-lg-6 bg-gray-100 rounded-lg">
          <podcast-history />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Provide, Prop } from "vue-property-decorator";

import Soundfx from "@/components/Podcast/Soundfx/index.vue";
import UserSoundfx from "@/components/Podcast/UserSoundfx/index.vue";
import ComposeTool from "@/components/Podcast/ComposeTool/index.vue";
import PodcastVisual from "@/components/Podcast/Visual/index.vue";
import PodcastHistory from "@/components/Podcast/History/index.vue";
import Recorder from "@/components/Podcast/Recorder/index.vue";

@Component({
  name: "podcast-compose-page",
  components: {
    Soundfx,
    UserSoundfx,
    ComposeTool,
    PodcastVisual,
    PodcastHistory,
    Recorder
  }
})
export default class PodcastComposePage extends Vue {}
</script>
