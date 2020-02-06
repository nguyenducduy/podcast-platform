<template>
  <a-pagination
    :size="options.size"
    :total="options.total"
    :current="options.current"
    :pageSize="options.pageSize"
    :showQuickJumper="options.showQuickJumper"
    hideOnSinglePage
    @change="onPageChange"
  />
</template>

<script lang="ts">
import { Vue, Component, Watch, Prop } from "vue-property-decorator";

@Component({
  name: "pagination"
})
export default class Pagination extends Vue {
  @Prop()
  routePath;

  @Prop()
  options;

  @Watch("$route")
  _routeChange() {
    const { page } = this.$route.query;
    const currentPage: any = typeof page !== "undefined" ? page : 1;
    this.options.current = parseInt(currentPage);
  }

  onPageChange(pageNumber) {
    this.$router.push(`/${this.routePath}?page=${pageNumber}`);
    window.scroll({
      top: 0,
      left: 0,
      behavior: "smooth"
    });
  }
}
</script>
