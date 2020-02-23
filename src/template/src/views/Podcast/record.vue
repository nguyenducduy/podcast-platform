<template>
  <div class="row">
    <div class="col-lg-6">
      <recorder />
    </div>
    <div class="col-lg-6">interview (may be use https://zoom.us/)</div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Provide, Prop } from "vue-property-decorator";
import Recorder from "@/components/Podcast/Recorder/index.vue";

@Component({
  name: "podcast-record-page",
  components: {
    Recorder
  }
})
export default class PodcastRecordPage extends Vue {}
</script>
