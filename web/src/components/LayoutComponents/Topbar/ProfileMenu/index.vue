<template>
  <a-dropdown :trigger="['click']" placement="bottomLeft">
    <div :class="$style.dropdown">
      <!-- <a-badge :count="count"> -->
      <a-avatar shape="square" icon="user" size="large" :class="$style.avatar" />
      <!-- </a-badge> -->
    </div>
    <a-menu slot="overlay">
      <a-menu-item>
        <div>
          <strong>Xin chào, {{ loggedUser.fullName }}</strong>
        </div>
        <div>
          <strong class="mr-1">Quyền:</strong>
          <a-tag :color="loggedUser.group.color">{{ loggedUser.group.screenName }}</a-tag>
        </div>
      </a-menu-item>
      <a-menu-divider />
      <a-menu-item>
        <div>
          <strong class="mr-1">Email:</strong>
          {{ loggedUser.email }}
        </div>
      </a-menu-item>
      <a-menu-divider />
      <a-menu-item>
        <router-link to="/admin/user/changepassword">
          <i :class="$style.menuIcon" class="icmn-key"></i> Đổi mật khẩu
        </router-link>
      </a-menu-item>
      <a-menu-item>
        <a href="javascript: void(0);" @click="onLogout">
          <i :class="$style.menuIcon" class="icmn-exit"></i> Đăng xuất
        </a>
      </a-menu-item>
    </a-menu>
  </a-dropdown>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { LOGOUT_USER } from "@/graphql/users";
import { Mutation as StoreMutation, Getter } from "vuex-class";

@Component({
  name: "profile-menu"
})
export default class ProfileMenu extends Vue {
  @StoreMutation("users/REMOVE_AUTH") removeAuth;
  @Getter("users/loggedUser") loggedUser;
  // count: Number = 99;

  async onLogout() {
    (this as any).$nprogress.start();

    try {
      const res = await this.$apollo.mutate({
        mutation: LOGOUT_USER
      });

      if (res && res.data.logoutUser !== null) {
        this.removeAuth();

        return (window.location.href = `
          ${window.location.protocol}//${window.location.hostname +
          (window.location.port ? ":" + window.location.port : "")}/admin
        `);
      }

      (this as any).$nprogress.done();
    } catch (error) {
      (this as any).$nprogress.done();

      this.$notification.error({
        message: "Lỗi trong quá trình đăng xuất",
        description: error.toString()
      });
    }
  }
}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
