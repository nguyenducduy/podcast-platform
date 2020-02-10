<template>
  <div :class="$style.visual" v-show="visible">
    <div id="wavesurfer-container" style="position: relative;"></div>
    <div id="timeline-container"></div>
    <a-button
      @click="onPlayPause"
      size="large"
      type="link"
      :icon="!playing ? `caret-right` : `pause`"
      style="font-size: 16px;"
    ></a-button>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus } from "@/helpers/utils";
import { sleep } from "@/helpers/utils";
import WaveSurfer from "wavesurfer.js";
import Cursor from "@/plugins/Wavesurfer/cursor";
import RegionPlugin from "@/plugins/Wavesurfer/region";
import TimelinePlugin from "wavesurfer.js/dist/plugin/wavesurfer.timeline";

@Component({
  name: "podcast-visual"
})
export default class PodcastVisual extends Vue {
  instance: any = null;
  playing: boolean = false;
  visible: boolean = false;

  onPlayPause() {
    this.playing ? this.instance.pause() : this.instance.play();
    this.playing = !this.playing;
  }

  created() {
    bus.$on("visual:render", async (track, regions) => {
      this.visible = true;

      this.instance.empty();
      this.instance.load(`${process.env.VUE_APP_MEDIA_URI}/${track.path}`);
      this.instance.drawBuffer();
      this.instance.clearRegions();

      await sleep(1000);
      regions.forEach(region => {
        this.instance.addRegion({
          start: region.start,
          end: region.end,
          color: region.color,
          drag: false,
          resize: false,
          attributes: {
            label: region.label
          }
        });
      });

      // console.log(this.instance.regions.list)
    });
  }

  mounted() {
    this.$nextTick(() => {
      this.instance = WaveSurfer.create({
        container: "#wavesurfer-container",
        height: 80,
        pixelRatio: 1,
        waveColor: "rgb(252, 194, 158)",
        // progressColor: "rgb(252, 194, 158)",
        cursorColor: "#fff",
        cursorWidth: 1,
        barWidth: 3,
        barRadius: 3,
        barGap: 3,
        backend: "MediaElement",
        mediaType: "audio",
        plugins: [
          Cursor.create({
            container: "#wavesurfer-container",
            showTime: true,
            opacity: 1,
            customShowTimeStyle: {
              "background-color": "#333",
              color: "#fff",
              "font-size": "11px"
            }
          } as any),
          RegionPlugin.create({
            color: "rgba(84, 197, 255, 0.44)"
          } as any),
          TimelinePlugin.create({
            container: "#timeline-container"
          } as any)
        ]
      });

      this.instance.on("region-click", region => {});

      this.instance.on("seek", seekTime => {
        const currentTime = seekTime * this.instance.getDuration();
        this.instance.play(currentTime);
        this.playing = true;
      });

      this.instance.on("audioprocess", progress => {
        if (parseInt(progress) == parseInt(this.instance.getDuration())) {
          this.playing = false;
        }
      });
    });
  }
}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
