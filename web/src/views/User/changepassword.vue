<template>
  <a-layout-content class="lg">
    <div class="utils__title mb-3">
      <strong class="text-uppercase font-size-16">Đổi mật khẩu</strong>
    </div>
    <div class="row">
      <div class="col-lg-4">
        <a-form class="mt-3" :form="form" @submit="onSubmit">
          <div class="row">
            <div class="col-lg-6">
              <a-form-item label="Mật khẩu mới" has-feedback>
                <a-input
                  type="password"
                  v-decorator="[
                      'password',
                      {
                        rules: [
                          {
                            required: true,
                            message: 'Vui lòng điền mật khẩu'
                          },
                          {
                            validator: validateToNextPassword
                          }
                        ]
                      }
                    ]"
                />
              </a-form-item>
            </div>
            <div class="col-lg-6">
              <a-form-item label="Nhập lại mật khẩu mới" has-feedback>
                <a-input
                  type="password"
                  @blur="handleConfirmPasswordBlur"
                  v-decorator="[
                      'confirm',
                      {
                        rules: [
                          {
                            required: true,
                            message: 'Vui lòng điền nhập lại mật khẩu'
                          },
                          {
                            validator: compareToFirstPassword
                          }
                        ]
                      }
                    ]"
                />
              </a-form-item>
            </div>
          </div>
        </a-form>
        <a-button
          type="primary"
          :style="{ marginRight: '8px' }"
          @click="onSubmit"
          :loading="loading"
        >Cập nhật</a-button>
      </div>
    </div>
  </a-layout-content>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { CHANGE_PASSWORD } from "@/graphql/users";

@Component({
  name: "user-changepassword-page"
})
export default class Changepassword extends Vue {
  form: any = {};
  loading: boolean = false;
  confirmDirty: boolean = false;

  handleConfirmPasswordBlur(e) {
    const value = e.target.value;
    this.confirmDirty = this.confirmDirty || !!value;
  }

  compareToFirstPassword(rule, value, callback) {
    const form = this.form;
    if (value && value !== form.getFieldValue("password")) {
      callback("2 mật khẩu không trùng nhau");
    } else {
      callback();
    }
  }

  validateToNextPassword(rule, value, callback) {
    const form = this.form;
    if (value && this.confirmDirty) {
      form.validateFields(["confirm"], { force: true });
    }
    callback();
  }

  onSubmit(e) {
    e.preventDefault();
    this.form.validateFields(async (err, values) => {
      if (!err) {
        this.loading = true;

        try {
          const res = await this.$apollo.mutate({
            mutation: CHANGE_PASSWORD,
            variables: {
              password: values.password
            }
          });

          if (res && res.data.changePassword !== null) {
            this.$notification.success({
              message: "Mật khẩu",
              description: `Đổi mật khẩu thành viên "${res.data.changePassword.user.fullName}" thành công`
            });

            this.form.resetFields();
            this.loading = false;
          }
        } catch (error) {
          this.loading = false;

          this.$notification.error({
            message: "Lỗi trong quá trình đổi mật khẩu",
            description: error.toString()
          });
        }
      }
    });
  }

  async created() {
    this.form = this.$form.createForm(this);
  }
}
</script>
