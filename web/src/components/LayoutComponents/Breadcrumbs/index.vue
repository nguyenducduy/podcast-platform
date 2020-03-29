<template>
  <div :class="$style.breadcrumbs">
    <div :class="$style.path">
      <template v-for="(item, index) in breadcrumb">
        <span v-if="index != 0" :key="index">
          <router-link
            :to="`/${item.key}`"
            class="text-muted font-weight-normal utils__link--underlined"
          >
            {{ item.title }}
          </router-link>
        </span>
      </template>
      <span v-if="activeItem">
        <span :class="$style.arrow"></span>
        <strong>{{ activeItem.title }}</strong>
      </span>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from "vue-property-decorator";
import { items } from "@/components/LayoutComponents/Menu/menu.json";
import { reduce } from "lodash";

@Component({
  name: "breadcrumbs"
})
export default class Breadcrumbs extends Vue {
  @Prop() settings;
  @Watch("$route")
  setBreadcrum(to) {
    this.breadcrumb = this.getPath(this.menuData, to.path);
  }

  menuData: any = items;
  breadcrumb: any = [];
  activeItem: any = {};
  path: any = [];

  getPath(data: any, url: string, parents: any = []) {
    if (url === "/") {
      url = "/dashboard";
    }
    const items = reduce(
      data,
      (result, entry) => {
        if (result.length) {
          return result;
        }
        if (entry.children) {
          const nested = this.getPath(
            entry.children,
            url,
            [entry].concat(parents)
          );
          return (result || []).concat(nested.filter(e => !!e));
        }
        if (entry.url === url) {
          return [entry].concat(parents);
        }
        return result;
      },
      []
    );
    this.activeItem = items[0];

    return items;
  }

  mounted() {
    this.breadcrumb = this.getPath(this.menuData, this.$route.path);
  }
}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
