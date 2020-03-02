<template>
  <h1>Edit filedrive</h1>
  <!-- <a-modal centered :maskClosable="false" v-model="visible" onOk="onSubmit" width="960px">
    <div slot="title">Sửa file #{{ filedriveId }}</div>
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
                      v-if="imageUrl"
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
    <template slot="footer">
      <a-button key="back" @click="onClose()">Huỷ</a-button>
      <a-button
        key="submit"
        type="primary"
        icon="save"
        :loading="$apollo.loading"
        @click="onSubmit"
      >Lưu</a-button>
    </template>
  </a-modal>-->
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus, getBase64, getVariables } from "@/helpers/utils";
// import { GET_FILEDRIVE, UPDATE_FILEDRIVE } from "@/graphql/podcasts";

@Component({
  name: "filedrive-edit-modal"
  // apollo: {
  //   filedriveGraph: {
  //     query: GET_FILEDRIVE,
  //     variables() {
  //       return { id: this.filedriveId };
  //     },
  //     update(data) {
  //       return data.getFiledrive;
  //     },
  //     skip() {
  //       return this.skipQuery;
  //     }
  //   }
  // }
})
export default class FiledriveEdit extends Vue {
  mediaUri: any = process.env.VUE_APP_MEDIA_URI;

  form: any = {};
  imageUrl: any = null;
  visible: boolean = false;

  filedriveId: number = 0;
  filedriveGraph: any = {
    edges: null
  };
  skipQuery: boolean = true;

  onClose() {
    this.visible = false;
  }

  onSubmit(e) {
    e.preventDefault();
    this.form.validateFields(async (err, values) => {
      if (!err) {
        // try {
        //   const res = await this.$apollo.mutate({
        //     mutation: UPDATE_PODCAST,
        //     variables: {
        //       podcastId: this.podcastId,
        //       title: values.title,
        //       description: this.summarize,
        //       status: parseInt(values.status),
        //       file: values.cover ? values.cover[0]["originFileObj"] : null,
        //       contactEmail: values.contactEmail,
        //       websiteUrl: values.websiteUrl,
        //       copyright: values.copyright
        //     }
        //   });
        //   if (res && res.data.createPodcast !== null) {
        //     this.$notification.success({
        //       message: "Cập nhật podcast thành công!",
        //       description: values.title,
        //       duration: 2
        //     });
        //     this.form.resetFields();
        //     this.imageUrl = null;
        //     this.visible = false;
        //     bus.$emit("podcast:refresh");
        //   }
        // } catch (error) {
        //   this.$notification.error({
        //     message: "Lỗi trong quá trình cập nhật!",
        //     description: error.toString(),
        //     duration: 5
        //   });
        //   return;
        // }
      }
    });
  }

  // created() {
  //   bus.$on("podcast:showEditModal", async podcastId => {
  //     this.podcastId = podcastId;
  //     this.$apollo.queries.podcastGraph.skip = false;
  //     const res = await this.$apollo.queries.podcastGraph.refetch();
  //     if (res) {
  //       const podcast = res.data.podcast;
  //       this.summarize = podcast.description;
  //       this.imageUrl = `${this.mediaUri}/${podcast.cover}`;

  //       this.form = this.$form.createForm(this, {
  //         mapPropsToFields: () => {
  //           return {
  //             title: this.$form.createFormField({
  //               value: podcast.title
  //             }),
  //             status: this.$form.createFormField({
  //               value: podcast.status.toString()
  //             }),
  //             contactEmail: this.$form.createFormField({
  //               value: podcast.contactEmail
  //             }),
  //             websiteUrl: this.$form.createFormField({
  //               value: podcast.websiteUrl
  //             }),
  //             copyright: this.$form.createFormField({
  //               value: podcast.copyright
  //             })
  //           };
  //         }
  //       });

  //       this.visible = true;
  //     }
  //   });
  // }
}
</script>
