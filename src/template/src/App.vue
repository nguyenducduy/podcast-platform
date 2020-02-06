<template>
  <div id="app">
    <component :is="layout">
      <router-view></router-view>
    </component>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
const default_layout = "main";

@Component({
  name: "app-page"
})
export default class App extends Vue {
  get layout() {
    return (this.$route.meta.layout || default_layout) + "-layout";
  }
}
</script>
