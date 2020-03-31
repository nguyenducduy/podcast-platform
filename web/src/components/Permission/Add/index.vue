<template>
  <div
    :style="{
      position: 'relative',
      float: 'right'
    }"
  >
    <a-button type="primary" icon="plus" @click="onShow">Thêm</a-button>
    <a-drawer
      title="Thêm quyền"
      placement="right"
      :visible="visible"
      :width="360"
      :closable="false"
      @close="onClose"
      :wrapStyle="{
        height: 'calc(100% - 108px)',
        overflow: 'auto',
        paddingBottom: '108px'
      }"
    >
      <div class="row">
        <div class="col-lg-12">
          <a-form class="mt-3" :form="form" @submit="onSubmit">
            <div class="row">
              <div class="col-lg-12">
                <a-form-item label="Tên (Query/Mutation)">
                  <a-input
                    placeholder="ex: userList, createUser"
                    v-decorator="[
                      'name',
                      {
                        rules: [
                          {
                            required: true,
                            message: 'Vui lòng điền tên!'
                          }
                        ]
                      }
                    ]"
                  />
                </a-form-item>
              </div>
              <div class="col-lg-12">
                <a-form-item label="Mô tả">
                  <a-textarea
                    v-decorator="[
                      'description',
                      {
                        rules: [
                          {
                            required: true,
                            message: 'Vui lòng điền mô tả!'
                          }
                        ]
                      }
                    ]"
                  />
                </a-form-item>
              </div>
            </div>
          </a-form>
        </div>
      </div>

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
        <a-button type="danger" :style="{ marginRight: '8px' }" @click="onClose"
          >Huỷ</a-button
        >
        <a-button
          type="primary"
          :style="{ marginRight: '8px' }"
          @click="onSubmit"
          :loading="loading"
          >Thêm</a-button
        >
      </div>
    </a-drawer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { CREATE_PERMISSION } from "@/graphql/permissions";
import { bus } from "@/helpers/utils";

@Component({
  name: "permission-add-drawer"
})
export default class PermissionAdd extends Vue {
  visible: boolean = false;
  form: any = {};
  loading: boolean = false;

  onShow() {
    this.visible = true;
  }

  onClose() {
    this.visible = false;
  }

  onSubmit(e) {
    e.preventDefault();
    this.form.validateFields(async (err, values) => {
      if (!err) {
        this.loading = true;

        try {
          const res = await this.$apollo.mutate({
            mutation: CREATE_PERMISSION,
            variables: {
              name: values.name,
              description: values.description
            }
          });

          if (res && res.data.createPermission !== null) {
            this.$notification.success({
              message: "Quyền",
              description: `Thêm quyền "${values.name}" thành công.`
            });

            this.form.resetFields();
            this.loading = false;
            bus.$emit("permission:refresh");
          }
        } catch (error) {
          this.loading = false;

          this.$notification.error({
            message: "Lỗi trong quá trình thêm quyền",
            description: error.toString()
          });
        }
      }
    });
  }

  created() {
    this.form = this.$form.createForm(this);
  }
}
</script>
