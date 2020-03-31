<template>
  <div :style="{
      position: 'relative'
    }">
    <a-drawer
      :title="`Sửa nhóm #${id}`"
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
                <a-form-item label="Tên (giá trị)">
                  <a-input
                    v-decorator="[
                    'name',
                    {
                      rules: [
                        {
                          required: true,
                          message: 'Vui lòng điền tên (giá trị)!'
                        }
                      ]
                    }
                  ]"
                  />
                </a-form-item>
              </div>
              <div class="col-lg-12">
                <a-form-item label="Tên (hiển thị)">
                  <a-input
                    v-decorator="[
                    'screenName',
                    {
                      rules: [
                        {
                          required: true,
                          message: 'Vui lòng điền tên (hiển thị)!'
                        }
                      ]
                    }
                  ]"
                  />
                </a-form-item>
              </div>
              <div class="col-lg-12">
                <a-form-item label="Màu thể hiện (hex, rgb, plain)">
                  <a-input
                    v-decorator="[
                    'color',
                    {
                      rules: [
                        {
                          required: true,
                          message: 'Vui lòng điền màu thể hiện!'
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
import { GET_GROUP, UPDATE_GROUP } from "@/graphql/groups";
import { bus } from "@/helpers/utils";

@Component({
  name: "group-edit-drawer",
  apollo: {
    groupGraph: {
      query: GET_GROUP,
      variables() {
        return { id: this.id };
      },
      update(data) {
        return data.getGroup;
      },
      skip() {
        return this.skipQuery;
      }
    }
  }
})
export default class GroupEdit extends Vue {
  visible: boolean = false;
  form: any = {};
  loading: boolean = false;
  id: number = 0;
  groupGraph: any = {
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
            mutation: UPDATE_GROUP,
            variables: {
              id: this.id,
              name: values.name,
              screenName: values.screenName,
              color: values.color
            }
          });

          if (res && res.data.updateGroup !== null) {
            this.$notification.success({
              message: "Cập nhật nhóm thành công!",
              description: values.screenName,
              duration: 5
            });

            this.form.resetFields();
            this.visible = false;
            this.loading = false;
            bus.$emit("group:refresh");
          }
        } catch (error) {
          this.loading = false;

          this.$notification.error({
            message: "Lỗi trong quá trình cập nhật nhóm thành viên!",
            description: error.toString(),
            duration: 5
          });
        }
      }
    });
  }

  created() {
    bus.$on("group:showEdit", async id => {
      this.id = id;
      this.$apollo.queries.groupGraph.skip = false;
      const res = await this.$apollo.queries.groupGraph.refetch();

      if (res) {
        const group = res.data.group;

        this.form = this.$form.createForm(this, {
          mapPropsToFields: () => {
            return {
              name: this.$form.createFormField({
                value: group.name
              }),
              screenName: this.$form.createFormField({
                value: group.screenName
              }),
              color: this.$form.createFormField({
                value: group.color
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
