<template>
  <div class="row">
    <div class="col-lg-12">
      <div id="waveform"></div>
      <div>
        <h5>Thu âm (chỉ âm thanh)</h5>
        <br />
        <a-button
          size="small"
          type="primary"
          @click="onStart"
          :disabled="recording"
          :loading="recording"
        >Bắt đầu</a-button>&nbsp;
        <a-button size="small" type="danger" @click="onStop" :disabled="!recording">Dừng</a-button>&nbsp;
        <a-button size="small" type="dashed" @click="onListen" :disabled="audioUrl === ''">Nghe</a-button>&nbsp;
        <a-button
          size="small"
          type="dashed"
          @click="onSave"
          :disabled="audioUrl === ''"
          :loading="uploading"
        >Lưu</a-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import RecordRTC from "recordrtc";
import WaveSurfer from "wavesurfer.js";
import MicrophonePlugin from "@/plugins/Wavesurfer/microphone";
import { RECORD_UPLOAD } from "@/graphql/filedrives";
import { bus } from "@/helpers/utils";

declare global {
  interface Window {
    stream: any;
    AudioContext: any;
    webkitAudioContext: any;
    MediaStreamRecorder: any;
  }
}
window.stream = window.stream || {};

@Component({
  name: "recorder"
})
export default class Recorder extends Vue {
  instance: any = null;
  context: any = new (window.AudioContext || window.webkitAudioContext)();
  processor: any = this.context.createScriptProcessor(1024, 1, 1);
  audioBlob: any = null;
  audioUrl: string = "";
  recorder: any = null;
  recording: boolean = false;
  uploading: boolean = false;

  onListen() {
    this.instance.playPause();
  }

  onStart() {
    this.recording = true;
    this.instance.microphone.start();
  }

  onStop() {
    this.recording = false;
    const self = this;
    this.instance.microphone.stop();
    this.recorder.stopRecording(audioURL => {
      self.audioUrl = audioURL;
      self.audioBlob = self.recorder.getBlob();
      self.instance.load(audioURL);
    });
  }

  async onSave() {
    this.uploading = true;

    let myFile = new File([this.audioBlob], "rec.wav", {
      type: "audio/wav"
    });

    try {
      const res = await this.$apollo.mutate({
        mutation: RECORD_UPLOAD,
        variables: {
          file: myFile
        }
      });

      if (res) {
        this.$notification.success({
          message: "Record upload success!",
          description: "",
          duration: 2
        });

        bus.$emit("userSoundfx:refresh");
      }

      this.uploading = false;
    } catch (error) {
      this.uploading = false;

      this.$notification.error({
        message: "Record upload failed!",
        description: error.toString(),
        duration: 5
      });
      return;
    }
  }

  mounted() {
    this.instance = WaveSurfer.create({
      container: "#waveform",
      interact: false,
      height: 50,
      waveColor: "rgb(252, 194, 158)",
      // progressColor: "rgb(252, 194, 158)",
      // cursorColor: "#fff",
      cursorWidth: 1,
      barWidth: 3,
      barRadius: 3,
      barGap: 3,
      audioContext: this.context,
      audioScriptProcessor: this.processor,
      mediaType: "audio",
      plugins: [
        MicrophonePlugin.create({
          bufferSize: 4096,
          numberOfInputChannels: 1,
          numberOfOutputChannels: 1,
          constraints: {
            video: false,
            audio: true
          }
        } as any)
      ]
    });

    const self = this;
    this.instance.microphone.on("deviceReady", stream => {
      self.recorder = RecordRTC(stream, {
        type: "audio",
        mimeType: "audio/wav",
        recorderType: window.MediaStreamRecorder,
        // only for audio track
        audioBitsPerSecond: 128000
      });
      self.recorder.startRecording();
    });

    this.instance.microphone.on("deviceError", code => {
      console.warn("Device error: " + code);
    });
  }
}
</script>

<style lang="scss"></style>
