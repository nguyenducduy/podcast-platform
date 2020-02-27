<template>
  <a-modal
    centered
    :maskClosable="false"
    v-model="visible"
    onOk="onSubmit"
    width="960px"
  >
    <div slot="title">Sửa Episode #{{ episodeId }}</div>
    <div class="row">
      <a-form class="mt-3" :form="form" @submit="onSubmit" layout="vertical">
        <div class="row p-3">
          <div class="col-lg-8">
            <div class="row">
              <div class="col-lg-4">
                <a-form-item>
                  <a-upload
                    class="podcast-cover-image-upload"
                    v-decorator="[
                      'cover',
                      {
                        valuePropName: 'fileList',
                        getValueFromEvent: normFile
                      }
                    ]"
                    :multiple="false"
                    listType="picture-card"
                    :beforeUpload="onBeforeUpload"
                    :showUploadList="false"
                  >
                    <img
                      v-if="imageUrl !== null"
                      :src="imageUrl"
                      alt="avatar"
                      onerror="this.onerror=null;this.src='/images/no-img.png';"
                    />
                    <a-icon v-else type="plus" />
                  </a-upload>
                </a-form-item>
                <p
                  class="text-sm text-gray-500 text-center"
                  style="margin-top: -25px;"
                >
                  Nhấn vào hình và chọn hình mới để thay đổi hình đại diện
                </p>
              </div>
              <div class="col-lg-8">
                <a-form-item label="Tiêu đề">
                  <a-input
                    v-decorator="[
                      'title',
                      {
                        rules: [
                          {
                            required: true,
                            message: 'Vui lòng điền tiêu đề!'
                          }
                        ]
                      }
                    ]"
                  />
                </a-form-item>
                <div class="row">
                  <div class="col-lg-6">
                    <a-form-item label="Trạng thái">
                      <a-select
                        v-decorator="[
                          'status',
                          {
                            rules: [
                              {
                                required: true,
                                message: 'Vui lòng chọn trạng thái!'
                              }
                            ]
                          }
                        ]"
                        placeholder="Chọn trạng thái"
                      >
                        <a-select-option value="3">Nháp</a-select-option>
                        <a-select-option value="1">Xuất bản</a-select-option>
                      </a-select>
                    </a-form-item>
                  </div>
                  <div class="col-lg-6">
                    <a-form-item label="Loại">
                      <a-select
                        v-decorator="[
                          'type',
                          {
                            rules: [
                              {
                                required: true,
                                message: 'Vui lòng chọn loại!'
                              }
                            ]
                          }
                        ]"
                        placeholder="Chọn loại"
                      >
                        <a-select-option value="1">Full</a-select-option>
                        <a-select-option value="3">Trailer</a-select-option>
                        <a-select-option value="5">Bonus</a-select-option>
                      </a-select>
                    </a-form-item>
                  </div>
                  <div class="col-lg-6">
                    <a-form-item label="Số thứ tự">
                      <a-input v-decorator="['orderNo']"></a-input>
                    </a-form-item>
                  </div>
                  <div class="col-lg-6">
                    <a-form-item label="Số Season">
                      <a-input v-decorator="['seasonNo']"></a-input>
                    </a-form-item>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-lg-4">
            <a-form-item label="Link">
              <a-input v-decorator="['link']"></a-input>
            </a-form-item>
            <a-form-item label="Tác giả">
              <a-input v-decorator="['author']"></a-input>
            </a-form-item>
          </div>
          <div class="col-lg-12">
            <a-form-item
              label="Description"
              class="mt-3"
              extra="This description may be used in several places including your RSS feed. Apple Podcasts will use this as your episode's description unless you set the `summary` field in your feed destination."
            >
              <div :class="$style.editor">
                <quill-editor
                  v-model="description"
                  :options="editorOption"
                ></quill-editor>
              </div>
            </a-form-item>
          </div>
        </div>
      </a-form>
    </div>
    <template slot="footer">
      <a-button key="back" @click="onClose()">Huỷ</a-button>
      <a-button
        key="submit"
        type="primary"
        icon="save"
        :loading="$apollo.loading"
        @click="onSubmit"
        >Lưu</a-button
      >
    </template>
  </a-modal>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus } from "@/helpers/utils";
import { getBase64 } from "@/helpers/utils";
import { GET_EPISODE, UPDATE_EPISODE } from "@/graphql/episodes";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";
import { quillEditor } from "vue-quill-editor";

@Component({
  name: "episode-edit-modal",
  components: {
    quillEditor
  },
  apollo: {
    episodeGraph: {
      query: GET_EPISODE,
      variables() {
        return { id: this.episodeId };
      },
      update(data) {
        return data.viewer.episode;
      },
      skip() {
        return this.skipQuery;
      }
    }
  }
})
export default class EpisodeEditModal extends Vue {
  mediaUri: any = process.env.VUE_APP_MEDIA_URI;

  form: any = {};
  imageUrl: any = null;
  visible: boolean = false;
  description: string = "";
  editorOption: any = {
    modules: {
      toolbar: true
    }
  };

  episodeId: number = 0;
  episodeGraph: any = {
    edges: null
  };
  skipQuery: boolean = true;

  onClose() {
    this.visible = false;
  }

  normFile(e) {
    if (Array.isArray(e)) {
      return e;
    }
    e.fileList.forEach(file => {
      getBase64(file.originFileObj, imageUrl => {
        this.imageUrl = imageUrl;
      });
    });
    return e && e.fileList;
  }

  onBeforeUpload(file) {
    return false;
  }

  onSubmit(e) {
    e.preventDefault();
    this.form.validateFields(async (err, values) => {
      if (!err) {
        try {
          const res = await this.$apollo.mutate({
            mutation: UPDATE_EPISODE,
            variables: {
              episodeId: this.episodeId,
              title: values.title,
              description: this.description,
              status: parseInt(values.status),
              type: parseInt(values.type),
              file: values.cover ? values.cover[0]["originFileObj"] : null,
              orderNo: parseInt(values.orderNo),
              seasonNo: parseInt(values.seasonNo),
              link: values.link,
              author: values.author
            }
          });

          if (res && res.data.updateEpisode !== null) {
            this.$notification.success({
              message: "Cập nhật Episode thành công!",
              description: values.title,
              duration: 2
            });

            this.form.resetFields();
            this.imageUrl = null;
            this.visible = false;
            bus.$emit("episode:refresh");
          }
        } catch (error) {
          this.$notification.error({
            message: "Lỗi trong quá trình cập nhật Episode!",
            description: error.toString(),
            duration: 5
          });
          return;
        }
      }
    });
  }

  created() {
    bus.$on("episode:showEditModal", async episodeId => {
      this.episodeId = episodeId;
      this.$apollo.queries.episodeGraph.skip = false;
      const res = await this.$apollo.queries.episodeGraph.refetch();
      if (res) {
        const episode = res.data.viewer.episode;
        this.description = episode.description;
        this.imageUrl = episode.cover
          ? `${this.mediaUri}/${episode.cover}`
          : null;

        this.form = this.$form.createForm(this, {
          mapPropsToFields: () => {
            return {
              title: this.$form.createFormField({
                value: episode.title
              }),
              status: this.$form.createFormField({
                value: episode.status.toString()
              }),
              type: this.$form.createFormField({
                value: episode.type.toString()
              }),
              orderNo: this.$form.createFormField({
                value: episode.orderNo
              }),
              seasonNo: this.$form.createFormField({
                value: episode.seasonNo
              }),
              link: this.$form.createFormField({
                value: episode.link
              })
            };
          }
        });

        this.visible = true;
      }
    });
  }
}
</script>

<style lang="scss" module>
@import "./add.module.scss";
</style>
