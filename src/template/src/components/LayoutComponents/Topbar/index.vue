<template>
  <div :class="$style.topbar">
    <div class="mr-auto">
      <live-search />
    </div>
    <div class="mr-4">
      <language-selector />
    </div>
    <profile-menu />
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import ProfileMenu from "@/components/LayoutComponents/Topbar/ProfileMenu/index.vue";
import LiveSearch from "@/components/LayoutComponents/Topbar/LiveSearch/index.vue";
import LanguageSelector from "@/components/LayoutComponents/Topbar/LanguageSelector/index.vue";

@Component({
  name: "topbar",
  components: {
    ProfileMenu,
    LiveSearch,
    LanguageSelector
  }
})
export default class Topbar extends Vue {}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
