<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";

@Component({
  name: "app-page"
})
export default class App extends Vue {}
</script>
<style>
#app {
  height: 100%;
}
</style>
