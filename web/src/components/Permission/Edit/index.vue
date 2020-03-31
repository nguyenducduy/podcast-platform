<template>
  <div :style="{
      position: 'relative'
    }">
    <a-drawer
      :title="`Sửa quyền #${id}`"
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
        <a-button type="danger" :style="{ marginRight: '8px' }" @click="onClose">Huỷ</a-button>
        <a-button
          type="primary"
          :style="{ marginRight: '8px' }"
          @click="onSubmit"
          :loading="loading"
        >Cập nhật</a-button>
      </div>
    </a-drawer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { GET_PERMISSION, UPDATE_PERMISSION } from "@/graphql/permissions";
import { bus } from "@/helpers/utils";

@Component({
  name: "permission-edit-drawer",
  apollo: {
    permissionGraph: {
      query: GET_PERMISSION,
      variables() {
        return { id: this.id };
      },
      update(data) {
        return data.getPermission;
      },
      skip() {
        return this.skipQuery;
      }
    }
  }
})
export default class PermissionEdit extends Vue {
  visible: boolean = false;
  form: any = {};
  loading: boolean = false;
  id: number = 0;
  permissionGraph: any = {
    edges: null
  };
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
            mutation: UPDATE_PERMISSION,
            variables: {
              id: this.id,
              name: values.name,
              description: values.description
            }
          });

          if (res && res.data.updatePermission !== null) {
            this.$notification.success({
              message: "Cập nhật quyền thành công!",
              description: values.screenName,
              duration: 5
            });

            this.form.resetFields();
            this.visible = false;
            this.loading = false;
            bus.$emit("permission:refresh");
          }
        } catch (error) {
          this.loading = false;

          this.$notification.error({
            message: "Lỗi trong quá trình cập nhật quyền!",
            description: error.toString(),
            duration: 5
          });
        }
      }
    });
  }

  created() {
    bus.$on("permission:showEdit", async id => {
      this.id = id;
      this.$apollo.queries.permissionGraph.skip = false;
      const res = await this.$apollo.queries.permissionGraph.refetch();

      if (res) {
        const permission = res.data.permission;

        this.form = this.$form.createForm(this, {
          mapPropsToFields: () => {
            return {
              name: this.$form.createFormField({
                value: permission.name
              }),
              description: this.$form.createFormField({
                value: permission.description
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
