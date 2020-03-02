<template>
  <div class="mb-3 mt-3">
    <a-upload
      :fileList="files"
      :multiple="true"
      :beforeUpload="beforeUpload"
      :remove="onRemove"
    >
      <a-button type="dashed" block> <a-icon type="desktop" />Upload </a-button>
    </a-upload>
    <a-button
      v-if="files.length > 0"
      style="margin-top: 10px;"
      block
      type="primary"
      @click="onUpload"
      :loading="loading"
      :disabled="files.length === 0"
    >
      <a-icon type="upload" />Upload
    </a-button>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus } from "@/helpers/utils";
import { UPLOAD } from "@/graphql/filedrives";

@Component({
  name: "podcast-upload"
})
export default class PodcastUpload extends Vue {
  files: any = [];
  loading: boolean = false;

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
    this.loading = true;
    const { files } = this;

    await Promise.all(
      files.map(async (file, index) => {
        try {
          let uploadedResponse = await this.$apollo.mutate({
            mutation: UPLOAD,
            variables: {
              file: file
            }
          });

          if (uploadedResponse) {
            this.files.splice(index, 1);

            this.$notification.success({
              message: "Upload success!",
              description: `${file.name}`,
              duration: 2
            });
          }
        } catch (error) {
          this.$notification.error({
            message: "Upload failed!",
            description: error.toString(),
            duration: 5
          });
        }
      })
    );

    this.files = [];
  }
}
</script>
