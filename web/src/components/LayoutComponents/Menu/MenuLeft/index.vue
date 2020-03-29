<template>
  <div>
    <div :class="$style.logo">
      <div :class="$style.logoContainer">
        <img src="/images/logo.png" alt />
      </div>
    </div>
    <div :class="[$style.navigation, $style.light]">
      <vue-custom-scrollbar
        :class="
          settings.isMobileView
            ? $style.scrollbarMobile
            : $style.scrollbarDesktop
        "
      >
        <a-menu
          ref="menu"
          :inlineCollapsed="withDrawer ? false : settings.isMenuCollapsed"
          mode="inline"
          @click="onClick"
          @openChange="onOpenChange"
          :selectedKeys="selectedKeys"
          :openKeys.sync="openKeys"
        >
          <template v-for="(item, index) in items">
            <a-menu-item
              :key="item.key"
              :disabled="item.disabled"
              v-if="!item.children && !item.divider"
            >
              <router-link v-if="item.url" :to="item.url">
                <i v-if="item.icon" :class="[$style.icon, item.icon]"></i>
                <span :class="$style.title">{{ item.title }}</span>
              </router-link>
              <span v-else>
                <i v-if="item.icon" :class="[$style.icon, item.icon]"></i>
                <span :class="$style.title">{{ item.title }}</span>
              </span>
            </a-menu-item>

            <a-menu-divider v-if="item.divider" :key="index" />

            <a-sub-menu v-if="item.children" :key="item.key">
              <span slot="title">
                <span :class="$style.title">{{ item.title }}</span>
                <i v-if="item.icon" :class="[$style.icon, item.icon]"></i>
              </span>
              <template v-for="(child, index) in item.children">
                <a-menu-item :key="child.key" :disabled="child.disabled">
                  <router-link v-if="child.url" :to="child.url">
                    <span :class="$style.title">{{ child.title }}</span>
                  </router-link>
                  <span v-else>
                    <span :class="$style.title">{{ child.title }}</span>
                  </span>
                </a-menu-item>
                <a-menu-divider v-if="child.divider" :key="index" />
              </template>
            </a-sub-menu>
          </template>
        </a-menu>
      </vue-custom-scrollbar>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from "vue-property-decorator";
import { Mutation, Getter } from "vuex-class";
import vueCustomScrollbar from "vue-custom-scrollbar";
import { items } from "@/components/LayoutComponents/Menu/menu.json";
import { find } from "lodash";

@Component({
  name: "menu-left",
  components: {
    vueCustomScrollbar
  }
})
export default class MenuLeft extends Vue {
  @Prop() settings;
  @Prop() withDrawer;
  @Mutation("SET") storeSet;
  @Watch("$route")
  routeChange() {
    this.setSelectedKeys();
  }
  @Watch("settings.isMenuCollapsed")
  menuCollapse() {
    this.openKeys = [];
  }
  @Getter("openKeys") getOpenKeys;
  @Getter("selectedKeys") getSelectedKeys;

  items: any = items;
  selectedKeys: any = [];
  openKeys: any = [];

  onClick(e) {
    this.storeSet({ app: "menu.selectedKeys", value: [e.key] });
    this.selectedKeys = [e.key];
  }
  onOpenChange(openKeys) {
    this.storeSet({ app: "menu.openedKeys", value: openKeys });
    this.openKeys = openKeys;
  }
  setSelectedKeys() {
    const pathname = this.$route.path;
    const menuData = this.items.concat();

    const flattenItems = (items, key) =>
      items.reduce((flattenedItems, item) => {
        flattenedItems.push(item);

        if (Array.isArray(item[key])) {
          return flattenedItems.concat(flattenItems(item[key], key));
        }

        return flattenedItems;
      }, []);

    const selectedItem = find(flattenItems(menuData, "children"), [
      "url",
      pathname
    ]);

    this.selectedKeys = selectedItem ? [selectedItem.key] : [];
    this.openKeys = [selectedItem.key.split("-")[0]];
  }

  created() {
    this.openKeys = this.getOpenKeys;
    this.selectedKeys = this.getSelectedKeys;
    this.setSelectedKeys();
  }
}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
