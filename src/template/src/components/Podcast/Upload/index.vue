<template>
  <div class="mb-3 mt-3">
    <a-upload
      :fileList="files"
      :multiple="true"
      :beforeUpload="beforeUpload"
      :remove="onRemove"
    >
      <a-button type="link" block>
        <a-icon type="desktop" />Upload từ máy tính
      </a-button>
    </a-upload>
    <a-button
      v-if="files.length > 0"
      style="margin-top: 10px;"
      block
      type="primary"
      @click="onUpload"
      :loading="$apollo.loading"
      :disabled="files.length === 0"
    >
      <a-icon type="upload" />Upload
    </a-button>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import gql from "graphql-tag";
import { bus } from "@/helpers/utils";
import { sleep } from "@/helpers/utils";
import { UPLOAD } from "@/graphql/filedrives";

@Component({
  name: "podcast-upload"
})
export default class PodcastUpload extends Vue {
  files: any = [];

  beforeUpload(file) {
    this.files = [...this.files, file];
    return false;
  }
  onRemove(file) {
    const index = this.files.indexOf(file);
    const newFiles = this.files.slice();
    newFiles.splice(index, 1);
    this.files = newFiles;
  }
  async onUpload() {
    const { files } = this;

    files.forEach(async (file, index) => {
      try {
        const res = await this.$apollo.mutate({
          mutation: UPLOAD,
          variables: {
            file: file
          }
        });

        if (res) {
          this.files.splice(index, 1);

          this.$notification.success({
            message: "Upload success!",
            description: `${file.name}`,
            duration: 2
          });

          bus.$emit("upload:success");
        }
      } catch (error) {
        this.$notification.error({
          message: "Upload failed!",
          description: error.toString(),
          duration: 5
        });
        return;
      }
    });

    await sleep(5000);
    this.files = [];
  }
}
</script>
