<template>
  <div :style="{
    position: 'relative',
    float: 'right'
  }">
    <a-button type="primary" icon="plus" @click="onShow">Thêm</a-button>
    <a-drawer
      title="Thêm người dùng"
      placement="right"
      :visible="visible"
      :width="640"
      :closable="false"
      @close="onClose"
      :wrapStyle="{
        height: 'calc(100% - 108px)',
        overflow: 'auto',
        paddingBottom: '108px'
      }"
    >
      <div
        :style="{
        position: 'absolute',
        left: 0,
        bottom: 0,
        width: '100%',
        borderTop: '1px solid #e9e9e9',
        padding: '10px 16px',
        background: '#fff',
        textAlign: 'right'
      }"
      >
        <a-button type="primary" :style="{ marginRight: '8px' }">Thêm</a-button>
        <a-button type="danger" :style="{ marginRight: '8px' }" @click="onClose">Huỷ</a-button>
      </div>
    </a-drawer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";

@Component({
  name: "user-add-drawer"
})
export default class UserAdd extends Vue {
  visible: boolean = false;

  onShow() {
    this.visible = true;
  }

  onClose() {
    this.visible = false;
  }
}
</script>
