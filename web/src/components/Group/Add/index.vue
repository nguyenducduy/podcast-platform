<template>
  <div
    :style="{
      position: 'relative',
      float: 'right'
    }"
  >
    <a-button type="primary" icon="plus" @click="onShow">Thêm</a-button>
    <a-drawer
      title="Thêm nhóm"
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
                    placeholder="ex: admin"
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
                    placeholder="ex: Administrator"
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
                    placeholder="ex: #fafafa, or blue/red"
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
import { CREATE_GROUP } from "@/graphql/groups";
import { bus } from "@/helpers/utils";

@Component({
  name: "group-add-drawer"
})
export default class GroupAdd extends Vue {
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
            mutation: CREATE_GROUP,
            variables: {
              name: values.name,
              screenName: values.screenName,
              color: values.color
            }
          });

          if (res && res.data.createGroup !== null) {
            this.$notification.success({
              message: "Nhóm thành viên",
              description: `Thêm nhóm "${values.screenName}" thành công`
            });

            this.form.resetFields();
            this.loading = false;
            bus.$emit("group:refresh");
          }
        } catch (error) {
          this.loading = false;

          this.$notification.error({
            message: "Lỗi trong quá trình thêm nhóm thành viên",
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
