<template>
  <div>
    <slot />
    <div :class="[$style.footer, 'text-center']">
      <p>&copy; 2019 MK Software. All rights reserved.</p>
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
