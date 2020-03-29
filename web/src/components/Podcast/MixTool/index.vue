<template>
  <div>
    <a-modal centered :maskClosable="false" v-model="visible">
      <template slot="title">
        mix
        <a-tag>{{ fromTrack.name }}</a-tag
        >to
        <a-tag color="rgb(252, 194, 158)">{{ toTrack.name }}</a-tag>
        <span v-if="mixStart !== null">
          at
          <strong>{{ mixStart }}</strong>
          <small>&nbsp; sec</small>
        </span>
      </template>
      <div :class="$style.visual">
        <!-- FROM TRACK -->
        <div class="row">
          <div class="col-lg-1" :class="$style.playBtnContainer">
            <!-- <a-button
              @click="onPlayPauseFromTrack"
              size="large"
              type="link"
              :icon="!fromTrackPlaying ? `caret-right` : `pause`"
            ></a-button>-->
          </div>
          <div class="col-lg-11">
            <div id="wavesurfer-mix-from-track-container"></div>
            <div id="timeline-mix-from-track-container"></div>
            <small>
              <i>{{ fromTrack.name }}</i>
            </small>
          </div>
          <div class="col-lg-1">
            <a-button
              @click="onPlayPauseRange"
              size="large"
              type="link"
              :icon="!rangePlaying ? `caret-right` : `pause`"
            ></a-button>
          </div>
          <div class="mb-4 col-lg-11">
            <a-slider
              range
              :defaultValue="[rangeStart, rangeEnd]"
              :min="minDuration"
              :max="maxDuration"
              @change="onSlideChange"
            />
            <small>
              Slide to set duration of
              <i>{{ fromTrack.name }}</i> mix to
              <i>{{ toTrack.name }}</i> track.
            </small>
          </div>
        </div>
        <!-- TO TRACK -->
        <div class="row">
          <div class="col-lg-1" :class="$style.playBtnContainer">
            <a-button
              @click="onPlayPauseToTrack"
              size="large"
              type="link"
              :icon="!toTrackPlaying ? `caret-right` : `pause`"
            ></a-button>
          </div>
          <div class="col-lg-11">
            <div id="wavesurfer-mix-to-track-container"></div>
            <div id="timeline-mix-to-track-container"></div>
            <small>
              <i>{{ toTrack.name }}</i>
            </small>
          </div>
        </div>
      </div>
      <template slot="footer">
        <div class="row">
          <!-- <div class="col-lg-6 text-left">
            <a-button type="dashed" @click="onTry()" :loading="loading">Try</a-button>
          </div>-->
          <div class="col-lg-12">
            <a-button @click="onClose">Close</a-button>
            <a-button type="primary" @click="onMix()" :loading="loading"
              >Mix</a-button
            >
          </div>
        </div>
      </template>
    </a-modal>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus, sleep } from "@/helpers/utils";
import WaveSurfer from "wavesurfer.js";
import Cursor from "@/plugins/Wavesurfer/cursor";
import TimelinePlugin from "wavesurfer.js/dist/plugin/wavesurfer.timeline";
import { find } from "lodash";
import { GET_FILES_TO_MIX } from "@/graphql/filedrives";
import { CREATE_REVISION } from "@/graphql/revisions";

@Component({
  name: "mix-tool",
  apollo: {
    filedriveGraph: {
      query: GET_FILES_TO_MIX,
      variables() {
        return {
          first: 2,
          fromTrack: this.fromTrack.id,
          toTrack: this.toTrack.id
        };
      },
      update(data) {
        return data.filedriveList;
      },
      skip() {
        return this.skipQuery;
      }
    }
  }
})
export default class MixTool extends Vue {
  instanceToTrack: any = null;
  instanceFromTrack: any = null;
  visible: boolean = false;
  filedriveGraph: any = {
    edges: null
  };

  fromTrack: any = {
    id: null,
    name: null,
    path: null,
    duration: null
  };
  toTrack: any = {
    id: null,
    name: null,
    path: null,
    duration: null
  };
  sessionId: string = "";

  skipQuery: boolean = true;
  fromTrackPlaying: boolean = false;
  toTrackPlaying: boolean = false;
  rangePlaying: boolean = false;

  minDuration: any = 0;
  maxDuration: any = 0;
  rangeStart: any = 0;
  rangeEnd: any = 0;
  mixStart: any = 0;
  rangeValue: any = [];
  loading: boolean = false;

  // async onTry() {
  //   this.loading = true;

  //   try {
  //     const res = await this.$apollo.mutate({
  //       mutation: CREATE_REVISION,
  //       variables: {
  //         sessionId: this.sessionId,
  //         content: JSON.stringify({
  //           type: "try",
  //           action: "mix",
  //           fdId: this.fromTrack.id,
  //           start: this.mixStart,
  //           duration: this.rangeValue
  //         })
  //       }
  //     });
  //   } catch (error) {
  //     this.$notification.error({
  //       message: "Fail to try mixed!",
  //       description: error.toString(),
  //       duration: 5
  //     });
  //   }

  //   this.loading = false;
  // }

  async onMix() {
    if (this.sessionId.length === 0) {
      alert("SESSION NULL");
      return;
    }
    this.loading = true;

    const res = await this.$apollo.mutate({
      mutation: CREATE_REVISION,
      variables: {
        sessionId: this.sessionId,
        content: JSON.stringify({
          type: "mix",
          action: "mix",
          fdId: this.fromTrack.id,
          start: this.mixStart,
          duration: this.rangeValue
        })
      }
    });

    this.loading = false;
    bus.$emit("composer:mixSuccess", res.data.createRevision.revision.version);
    //reset variable range and mixstart

    this.visible = false;
  }

  onSlideChange(val) {
    this.instanceFromTrack.setCurrentTime(val[0]);
    this.rangeValue = [val[0], val[1]];
  }
  onPlayPauseRange() {
    this.rangePlaying
      ? this.instanceFromTrack.pause()
      : this.instanceFromTrack.play(this.rangeValue[0], this.rangeValue[1]);
    this.rangePlaying = !this.rangePlaying;
  }

  onPlayPauseFromTrack() {
    this.fromTrackPlaying
      ? this.instanceFromTrack.pause()
      : this.instanceFromTrack.play();
    this.fromTrackPlaying = !this.fromTrackPlaying;
  }
  onPlayPauseToTrack() {
    this.toTrackPlaying
      ? this.instanceToTrack.pause()
      : this.instanceToTrack.play();
    this.toTrackPlaying = !this.toTrackPlaying;
  }

  onClose() {
    this.visible = false;
  }

  created() {
    bus.$on("mixtool:show", async (fromTrack, toTrack, sessionId) => {
      this.sessionId = sessionId;
      this.fromTrack = fromTrack;
      this.toTrack = toTrack;

      this.$apollo.queries.filedriveGraph.skip = false;
      await this.$apollo.queries.filedriveGraph.refetch();

      const ft = find(this.filedriveGraph.edges, o => {
        return o.node.id == fromTrack.id;
      });
      this.fromTrack = ft.node;

      const tt = find(this.filedriveGraph.edges, o => {
        return o.node.id == toTrack.id;
      });
      this.toTrack = tt.node;

      this.maxDuration = Math.ceil(ft.node.duration);
      this.rangeEnd = parseFloat(ft.node.duration);
      this.rangeValue = [0, this.rangeEnd];
      this.visible = true;
    });
  }

  async updated() {
    // FROM TRACK
    const countReadyFromTrackWaveDom = document.querySelectorAll(
      "#wavesurfer-mix-from-track-container"
    ).length;
    if (countReadyFromTrackWaveDom === 1 && this.instanceFromTrack === null) {
      this.instanceFromTrack = WaveSurfer.create({
        container: "#wavesurfer-mix-from-track-container",
        height: 80,
        pixelRatio: 1,
        waveColor: "#000",
        cursorColor: "#f50",
        cursorWidth: 1,
        barWidth: 3,
        barRadius: 3,
        barGap: 3,
        backend: "MediaElement",
        mediaType: "audio",
        plugins: [
          Cursor.create({
            container: "#wavesurfer-mix-from-track-container",
            opacity: 1,
            showTime: true,
            customShowTimeStyle: {
              "background-color": "#333",
              color: "#fff",
              "font-size": "11px",
              top: 0
            }
          } as any),
          TimelinePlugin.create({
            container: "#timeline-mix-from-track-container"
          } as any)
        ]
      });

      this.instanceFromTrack.load(
        `${process.env.VUE_APP_MEDIA_URI}/${this.fromTrack.path}`
      );

      this.instanceFromTrack.on("audioprocess", progress => {
        if (progress == this.rangeValue[1]) {
          this.rangePlaying = false;
        }

        if (parseInt(progress) == parseInt(this.rangeEnd)) {
          this.fromTrackPlaying = false;
        }
      });
    }

    // TO TRACK
    const countReadyToTrackWaveDom = document.querySelectorAll(
      "#wavesurfer-mix-to-track-container"
    ).length;
    if (countReadyToTrackWaveDom === 1 && this.instanceToTrack === null) {
      this.instanceToTrack = WaveSurfer.create({
        container: "#wavesurfer-mix-to-track-container",
        height: 80,
        pixelRatio: 1,
        waveColor: "rgb(252, 194, 158)",
        cursorColor: "#f50",
        cursorWidth: 1,
        barWidth: 3,
        barRadius: 3,
        barGap: 3,
        backend: "MediaElement",
        mediaType: "audio",
        plugins: [
          Cursor.create({
            container: "#wavesurfer-mix-to-track-container",
            opacity: 1,
            showTime: true,
            customShowTimeStyle: {
              "background-color": "#333",
              color: "#fff",
              "font-size": "11px"
            }
          } as any),
          TimelinePlugin.create({
            container: "#timeline-mix-to-track-container"
          } as any)
        ]
      });

      this.instanceToTrack.load(
        `${process.env.VUE_APP_MEDIA_URI}/${this.toTrack.path}`
      );

      this.instanceToTrack.on("seek", seekTime => {
        const currentTime = seekTime * this.instanceToTrack.getDuration();
        this.mixStart = parseFloat(currentTime.toFixed(6));
      });

      this.instanceToTrack.on("audioprocess", progress => {
        if (
          parseInt(progress) == parseInt(this.instanceToTrack.getDuration())
        ) {
          this.toTrackPlaying = false;
        }
      });
    }
  }
}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
