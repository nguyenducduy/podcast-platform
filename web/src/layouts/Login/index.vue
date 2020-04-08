<template>
  <div>
    <router-view />
    <div :class="[$style.footer, 'text-center']" style="background-color: #f2f4f8">
      <p>&copy; 2019 OLLI Technology. All rights reserved.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";

@Component
export default class LoginLayout extends Vue {}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
