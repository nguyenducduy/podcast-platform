<template>
  <a-modal
    centered
    :maskClosable="false"
    destroyOnClose
    v-model="visible"
    onOk="onSubmit"
    width="960px"
  >
    <div slot="title">Import từ Apple Podcast</div>
    <div class="row">
      <div class="col-lg-12">
        <p>Nhập Apple Podcast URL vào khung bên dưới và nhấn Import</p>
        <small
          >Ví dụ:
          https://podcasts.apple.com/podcast/cryptoshow-blockchain-cryptocurrencies-bitcoin-decentralization/id1323952161</small
        >
        <a-input-search allowClear @search="onImport">
          <a-button
            slot="enterButton"
            type="primary"
            :loading="processing"
            :disabled="processing"
            >Import</a-button
          >
        </a-input-search>
      </div>
    </div>
  </a-modal>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus } from "@/helpers/utils";
import { IMPORT_FROM_APPLE } from "@/graphql/podcasts";

@Component({
  name: "apple"
})
export default class Apple extends Vue {
  visible: boolean = false;
  processing: boolean = false;

  async onImport(value) {
    var matches = value.match(/.*\/id(\d+)/);
    if (matches !== null) {
      const id = matches[1];

      try {
        this.processing = true;

        await this.$apollo.mutate({
          mutation: IMPORT_FROM_APPLE,
          variables: {
            id: id
          }
        });

        this.processing = false;

        this.$notification.success({
          message: "Import thành công!",
          description: "",
          duration: 5
        });

        this.visible = false;
        bus.$emit("podcast:refresh");
      } catch (error) {
        this.processing = false;

        this.$notification.error({
          message: "Lỗi trong quá trình import!",
          description: error.toString(),
          duration: 10
        });
        return;
      }
    } else {
      this.processing = false;

      this.$notification.warning({
        message: "Không tìm thấy Apple Podcast ID trong link này",
        description: "Vui lòng thử link khác",
        duration: 2
      });
    }
  }

  onClose() {
    this.visible = false;
  }

  created() {
    bus.$on("podcast:showImportFromAppleModal", () => {
      this.visible = true;
    });
  }
}
</script>
