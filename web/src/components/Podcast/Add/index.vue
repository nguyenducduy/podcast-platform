<template>
  <div :style="{
    position: 'relative',
    float: 'right'
  }">
    <a-button type="primary" icon="plus" @click="onShow">Thêm</a-button>
    <a-drawer
      title="Thêm podcast"
      placement="right"
      :visible="visible"
      :width="768"
      :closable="false"
      @close="onClose"
      :wrapStyle="{
        height: 'calc(100% - 108px)',
        overflow: 'auto',
        paddingBottom: '108px'
      }"
    >
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
                      <img v-if="imageUrl" :src="imageUrl" alt="avatar" />
                      <a-icon v-else type="plus" />
                    </a-upload>
                  </a-form-item>
                  <p
                    class="text-sm text-gray-500 text-center"
                    style="margin-top: -25px;"
                  >Nhấn vào hình và chọn hình mới để thay đổi hình đại diện</p>
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
              </div>
            </div>
            <div class="col-lg-4">
              <a-form-item label="Email liên hệ">
                <a-input v-decorator="['contactEmail']" placeholder="someone@gmail.com"></a-input>
              </a-form-item>
              <a-form-item label="Website URL">
                <a-input v-decorator="['websiteUrl']" placeholder="http|https://somedomain.com"></a-input>
              </a-form-item>
              <a-form-item label="Copyright">
                <a-input v-decorator="['copyright']" placeholder="All right reserved"></a-input>
              </a-form-item>
            </div>
            <div class="col-lg-12">
              <a-form-item
                label="Mô tả / Tóm tắt"
                class="mt-3"
                extra="This description may be used in several places including your RSS feed. Apple Podcasts will use this as your episode's description unless you set the `summary` field in your feed destination."
              >
                <div :class="$style.editor">
                  <quill-editor v-model="summarize" :options="editorOption"></quill-editor>
                </div>
              </a-form-item>
            </div>
          </div>
        </a-form>
      </div>
      <!-- // control button -->
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
        <a-button type="danger" :style="{ marginRight: '8px' }" @click="onClose">Huỷ</a-button>
        <a-button
          type="primary"
          :style="{ marginRight: '8px' }"
          @click="onSubmit"
          :loading="loading"
        >Thêm</a-button>
      </div>
    </a-drawer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { getBase64 } from "@/helpers/utils";
import { bus } from "@/helpers/utils";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";
import { quillEditor } from "vue-quill-editor";
import { CREATE_PODCAST } from "@/graphql/podcasts";

@Component({
  name: "podcast-add-drawer",
  components: {
    quillEditor
  }
})
export default class PodcastAdd extends Vue {
  visible: boolean = false;
  form: any = {};
  imageUrl: any = null;
  summarize: string = "";
  editorOption: any = {
    modules: {
      toolbar: true
    }
  };
  loading: boolean = false;

  onShow() {
    this.visible = true;
  }

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
        this.loading = true;

        try {
          const res = await this.$apollo.mutate({
            mutation: CREATE_PODCAST,
            variables: {
              title: values.title,
              description: this.summarize,
              status: parseInt(values.status),
              file: values.cover ? values.cover[0]["originFileObj"] : null,
              contactEmail: values.contactEmail,
              websiteUrl: values.websiteUrl,
              copyright: values.copyright
            }
          });

          if (res && res.data.createPodcast !== null) {
            this.$notification.success({
              message: "Thêm podcast thành công!",
              description: values.title,
              duration: 5
            });

            this.form.resetFields();
            this.imageUrl = null;
            this.visible = false;
            bus.$emit("podcast:refresh");
          }

          this.loading = false;
        } catch (error) {
          this.loading = false;

          this.$notification.error({
            message: "Lỗi trong quá trình thêm podcast!",
            description: error.toString(),
            duration: 5
          });

          return;
        }
      }
    });
  }

  created() {
    this.form = this.$form.createForm(this);
  }
}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
