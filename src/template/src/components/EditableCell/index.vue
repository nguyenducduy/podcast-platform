<template>
  <div class="editable-cell">
    <div v-if="editable" class="editable-cell-input-wrapper">
      <a-input :value="value" @change="handleChange" @pressEnter="check" :size="size || ''" />
      <a-icon type="check" class="editable-cell-icon-check" @click="check" />
    </div>
    <div v-else class="editable-cell-text-wrapper">
      {{ value || '' }}
      <a-icon type="edit" class="editable-cell-icon" @click="edit" />
    </div>
  </div>
</template>
<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";

@Component({
  name: "editable-cell"
})
export default class EditableCell extends Vue {
  @Prop() text: string;
  @Prop() size: string;

  value: string = this.text;
  editable: boolean = false;

  handleChange(e) {
    const value = e.target.value;
    this.value = value;
  }
  check() {
    this.editable = false;
    this.$emit("change", this.value);
  }
  edit() {
    this.editable = true;
  }
}
</script>
