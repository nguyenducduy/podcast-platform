<template>
  <a-dropdown :trigger="['click']" placement="bottomLeft">
    <div :class="$style.dropdown">
      <a-badge :count="count">
        <a-avatar
          shape="square"
          icon="user"
          size="large"
          :class="$style.avatar"
        />
      </a-badge>
    </div>
    <a-menu slot="overlay">
      <a-menu-item>
        <div>
          <strong>Xin chào, Administrator</strong>
        </div>
        <!-- <div><strong class="mr-1">Billing Plan:</strong> Professional</div> -->
        <div><strong class="mr-1">Quyền:</strong> Admin</div>
      </a-menu-item>
      <a-menu-divider />
      <a-menu-item>
        <div><strong class="mr-1">Email:</strong> admin@mksoftware.com</div>
        <div><strong class="mr-1">Di động:</strong> -</div>
      </a-menu-item>
      <a-menu-divider />
      <a-menu-item>
        <router-link to="/user/changepassword">
          <i :class="$style.menuIcon" class="icmn-user"></i> Đổi mật khẩu
        </router-link>
      </a-menu-item>
      <a-menu-item>
        <a href="javascript: void(0);">
          <i :class="$style.menuIcon" class="icmn-exit"></i> Đăng xuất
        </a>
      </a-menu-item>
    </a-menu>
  </a-dropdown>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";

@Component({
  name: "profile-menu"
})
export default class ProfileMenu extends Vue {
  count: Number = 99;
}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
