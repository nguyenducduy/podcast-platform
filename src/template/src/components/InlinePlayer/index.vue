<template>
  <a-button type="link" :icon="playing ? 'pause' : 'caret-right'" @click="onPlayPause"></a-button>
</template>

<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";

@Component({
  name: "inline-player"
})
export default class InlinePlayer extends Vue {
  @Prop() url: string;
  playing: boolean = false;
  player: any = null;

  onPlayPause() {
    if (this.playing === true && this.player !== null) {
      this.player.pause();
      this.playing = false;
    } else if (this.playing === false && this.player !== null) {
      this.player.play();
      this.playing = true;
    } else {
      const mySound = new window.Audio(this.url);
      mySound.play();
      this.playing = true;
      this.player = mySound;
      this.player.addEventListener("ended", () => {
        this.playing = false;
      });
    }
  }
}
</script>
