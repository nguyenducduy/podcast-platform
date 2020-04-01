<template>
  <div
    :style="{
      position: 'relative'
    }"
  >
    <a-drawer
      :title="`Sửa thành viên #${id}`"
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
                    >
                      {{ group.node.screenName }}
                    </a-select-option>
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
        <a-button type="danger" :style="{ marginRight: '8px' }" @click="onClose"
          >Huỷ</a-button
        >
        <a-button
          type="primary"
          :style="{ marginRight: '8px' }"
          @click="onSubmit"
          :loading="loading"
          >Cập nhật</a-button
        >
      </div>
    </a-drawer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { bus } from "@/helpers/utils";
import { GET_GROUPS } from "@/graphql/groups";
import { GET_USER, UPDATE_USER } from "@/graphql/users";

@Component({
  name: "user-edit-drawer",
  apollo: {
    userGraph: {
      query: GET_USER,
      variables() {
        return { id: this.id };
      },
      update(data) {
        return data.user;
      },
      skip() {
        return this.skipQuery;
      }
    }
  }
})
export default class UserEdit extends Vue {
  visible: boolean = false;
  form: any = {};
  loading: boolean = false;
  groupList: any = [];
  id: number = 0;
  userGraph: any = {};
  skipQuery: boolean = true;

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
            mutation: UPDATE_USER,
            variables: {
              id: this.id,
              fullName: values.fullName,
              email: values.email,
              groupId: values.groupId
            }
          });

          if (res && res.data.updateUser !== null) {
            this.$notification.success({
              message: "Thành viên",
              description: `Cập nhật thành viên "${values.fullName}" thành công`
            });

            this.form.resetFields();
            this.loading = false;
            this.visible = false;
            bus.$emit("user:refresh");
          }
        } catch (error) {
          this.loading = false;

          this.$notification.error({
            message: "Lỗi trong quá trình cập nhật thành viên",
            description: error.toString()
          });
        }
      }
    });
  }

  async created() {
    bus.$on("user:showEdit", async id => {
      this.id = id;
      this.$apollo.queries.userGraph.skip = false;
      const res = await this.$apollo.queries.userGraph.refetch();

      if (res) {
        const user = res.data.user;

        this.form = this.$form.createForm(this, {
          mapPropsToFields: () => {
            return {
              fullName: this.$form.createFormField({
                value: user.fullName
              }),
              email: this.$form.createFormField({
                value: user.email
              }),
              groupId: this.$form.createFormField({
                value: user.group.id
              })
            };
          }
        });

        this.visible = true;
      }
    });

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
