<template>
  <div :style="{
      position: 'relative',
      float: 'right'
    }">
    <a-button type="primary" icon="plus" @click="onShow">Thêm thành viên</a-button>
    <a-drawer
      title="Thêm thành viên"
      placement="right"
      :visible="visible"
      :width="640"
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
              <div class="col-lg-6">
                <a-form-item label="Họ và tên">
                  <a-input
                    v-decorator="[
                      'fullName',
                      {
                        rules: [
                          {
                            required: true,
                            message: 'Vui lòng điền họ và tên'
                          }
                        ]
                      }
                    ]"
                  />
                </a-form-item>
              </div>
              <div class="col-lg-6">
                <a-form-item label="Email">
                  <a-input
                    v-decorator="[
                      'email',
                      {
                        rules: [
                          {
                            type: 'email',
                            message: 'Email không hợp lệ'
                          },
                          {
                            required: true,
                            message: 'Vui lòng điền email'
                          }
                        ]
                      }
                    ]"
                  />
                </a-form-item>
              </div>
              <div class="col-lg-6">
                <a-form-item label="Mật khẩu" has-feedback>
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
                <a-form-item label="Nhập lại mật khẩu" has-feedback>
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
              <div class="col-lg-6">
                <a-form-item label="Nhóm">
                  <a-select
                    v-decorator="[
                      'groupId',
                      {
                        rules: [
                          {
                            required: true,
                            message: 'Vui lòng chọn nhóm'
                          }
                        ]
                      }
                    ]"
                    placeholder="Chọn nhóm"
                  >
                    <a-select-option
                      v-for="group in groupList.edges"
                      :value="group.node.id"
                      :key="group.node.id"
                    >{{ group.node.screenName }}</a-select-option>
                  </a-select>
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
import { bus } from "@/helpers/utils";
import { GET_GROUPS, GET_GROUP } from "@/graphql/groups";
import { CREATE_USER } from "@/graphql/users";

@Component({
  name: "user-add-drawer"
})
export default class UserAdd extends Vue {
  visible: boolean = false;
  form: any = {};
  loading: boolean = false;
  confirmDirty: boolean = false;
  groupList: any = [];

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
            mutation: CREATE_USER,
            variables: {
              fullName: values.fullName,
              email: values.email,
              password: values.password,
              groupId: values.groupId
            }
          });

          if (res && res.data.createUser !== null) {
            this.$notification.success({
              message: "Thành viên",
              description: `Thêm "${values.fullName}" thành công`
            });

            this.form.resetFields();
            this.loading = false;
            this.visible = false;
            bus.$emit("user:refresh");
          }
        } catch (error) {
          this.loading = false;

          this.$notification.error({
            message: "Lỗi trong quá trình thêm thành viên",
            description: error.toString()
          });
        }
      }
    });
  }

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

  async created() {
    this.form = this.$form.createForm(this);
    const res = await this.$apollo.query({
      query: GET_GROUPS,
      variables: {
        first: 1000,
        last: 1000
      }
    });

    if (res && res.data.groupList !== null) {
      this.groupList = res.data.groupList;
    } else {
      this.$notification.error({
        message: "Group",
        description: "Failed to load groupList"
      });
    }
  }
}
</script>
