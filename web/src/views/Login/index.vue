<template>
  <div style="background-color: #f2f4f8">
    <div :class="$style.block">
      <div class="row">
        <div class="col-xl-12">
          <div :class="$style.inner">
            <div :class="$style.form">
              <a-form class="login-form" :form="form" @submit="onSubmit">
                <a-form-item label="Email">
                  <a-input
                    placeholder="Email"
                    v-decorator="[
                      'email',
                      {
                        rules: [
                          {
                            required: true,
                            message: 'Please input your email!'
                          }
                        ]
                      }
                    ]"
                  >
                    <a-icon
                      slot="prefix"
                      type="user"
                      style="color: rgba(0,0,0,.25);"
                    />
                  </a-input>
                </a-form-item>
                <a-form-item label="Password">
                  <a-input
                    placeholder="Password"
                    type="password"
                    v-decorator="[
                      'password',
                      {
                        rules: [
                          {
                            required: true,
                            message: 'Please input your Password!'
                          }
                        ]
                      }
                    ]"
                  >
                    <a-icon
                      slot="prefix"
                      type="lock"
                      style="color: rgba(0,0,0,.25);"
                    />
                  </a-input>
                </a-form-item>
                <div>
                  <a-checkbox>Remember me</a-checkbox>
                  <router-link
                    class="pull-right text-primary utils__link--blue utils__link--underlined"
                    to="/user/forgot"
                    >Forgot password?</router-link
                  >
                </div>
                <div class="form-actions">
                  <a-button
                    type="primary"
                    htmlType="submit"
                    class="login-form-button width-150"
                    :loading="loading"
                    >Sign in</a-button
                  >
                </div>
                <div class="form-group">
                  <p>Use another service to Log In</p>
                  <div class="mt-2">
                    <a href="javascript: void(0);" class="btn btn-icon mr-2">
                      <i class="icmn-facebook" />
                    </a>
                    <a href="javascript: void(0);" class="btn btn-icon mr-2">
                      <i class="icmn-google" />
                    </a>
                  </div>
                </div>
              </a-form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { Mutation as StoreMutation } from "vuex-class";
import { LOGIN_BY_EMAIL } from "@/graphql/users";

@Component({
  name: "admin-login-page"
})
export default class AdminLogin extends Vue {
  @StoreMutation("users/SET_AUTH") setAuth;
  form: any = {};
  loading: boolean = false;

  created() {
    this.form = this.$form.createForm(this);
  }

  onSubmit(e) {
    e.preventDefault();
    this.form.validateFields(async (err, values) => {
      if (!err) {
        this.loading = true;

        try {
          const resp = await this.$apollo.mutate({
            mutation: LOGIN_BY_EMAIL,
            variables: {
              email: values.email,
              password: values.password
            }
          });

          if (resp.data !== null) {
            this.setAuth({
              user: resp.data.loginUser.user,
              token: resp.data.loginUser.token
            });

            const redirectUrl: any = this.$route.query.redirect || "";

            return (window.location.href = `
              ${window.location.protocol}//${window.location.hostname +
              (window.location.port
                ? ":" + window.location.port
                : "")}${redirectUrl}
            `);
          }

          this.loading = false;
        } catch (err) {
          this.loading = false;

          this.$notification.error({
            message: "Login failed.",
            description: err.toString(),
            duration: 5
          });
        }
      }
    });
  }
}
</script>

<style lang="scss" module>
@import "./style.module.scss";
</style>
