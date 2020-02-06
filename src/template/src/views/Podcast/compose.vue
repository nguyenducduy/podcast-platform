<template>
  <div class="row">
    <div class="col-lg-4 bg-gray-100 rounded-lg">
      <podcast-upload />
      <soundfx />
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
    <div class="w-full">
      <a-affix :offsetBottom="0">
        <podcast-visual />
      </a-affix>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Provide, Prop } from "vue-property-decorator";
import PodcastUpload from "@/components/Podcast/Upload/index.vue";
import Soundfx from "@/components/Podcast/Soundfx/index.vue";
import ComposeTool from "@/components/Podcast/ComposeTool/index.vue";
import PodcastVisual from "@/components/Podcast/Visual/index.vue";
import PodcastHistory from "@/components/Podcast/History/index.vue";

@Component({
  name: "podcast-compose-page",
  components: {
    PodcastUpload,
    Soundfx,
    ComposeTool,
    PodcastVisual,
    PodcastHistory
  }
})
export default class PodcastComposePage extends Vue {}
</script>
