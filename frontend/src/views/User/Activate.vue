<template>
  <div class="max-w-6xl mx-auto mt-8 mb-8 text-center"> 
    <h1>Activating Account...</h1>
    <p v-if="loading">Please wait...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="user && !loading">Account activated for {{ user.firstName }} {{ user.lastName }}. Redirecting...</p>
  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  name: "Activate",
  props: ['token', 'email'],
  data() {
    return {
      loading: true,
      error: null,
      user: null,
    };
  },
  methods: {
    async login() {
      // Clear previous errors
      this.error = null;

      try {
        const { data } = await this.$apollo.mutate({
          mutation: gql`
            mutation LoginUser($email: String!) {
              loginUser(input: { email: $email }) {
                token
                user {
                  id
                  email
                  admin
                  activated
                }
                errors
              }
            }
          `,
          variables: {
            email: this.email,
          },
        });

        if (data.loginUser.errors.length) {
          this.error = data.loginUser.errors.join(', ');
        } else {
          const token = data.loginUser.token;
          const userId = data.loginUser.user.id;
          localStorage.setItem('token', token);

          const redirectTo = JSON.parse(sessionStorage.getItem('redirectAfterLogin'));
          sessionStorage.removeItem('redirectAfterLogin'); // Clean up redirect URL

          // Check if the user is an admin
          const adminCheck = await this.$apollo.query({
            query: gql`
              query IsUserAdmin($id: ID!) {
                isAdmin(id: $id)
              }
            `,
            variables: {
              id: userId,
            },
          });

          const isAdmin = adminCheck.data.isAdmin;
          console.log("IS ADMIN: ", isAdmin);

          // Redirect based on admin status
          if (isAdmin) {
            this.$router.push({ 
              name: 'Dashboard', 
              query: { successMessage: 'Successfully logged in as admin' }
            });
          } else {
            if (redirectTo) {
              // Redirect to the original URL with success message
              this.$router.push({ 
                name: redirectTo.name, 
                params: redirectTo.params, 
                query: { ...redirectTo.query, successMessage: 'Successfully logged in' }
              });
            } else {
              // Redirect to home with success message if no original URL was stored
              this.$router.push({ 
                name: 'Home', 
                query: { successMessage: 'Successfully logged in' }
              });
            }
          }
        }
      } catch (error) {
        console.error(error.message);
        this.error = 'An error occurred while logging in.';
      }
    }
  },
  async created() {
    try {
      const { data } = await this.$apollo.mutate({
        mutation: gql`
          mutation ActivateAccount($token: String!, $email: String!) {
            activateAccount(input: { token: $token, email: $email }) {
              user {
                id
                firstName
                lastName
              }
              errors
            }
          }
        `,
        variables: {
          token: this.token,
          email: this.email,
        },
      });

      if (data.activateAccount.errors.length) {
        this.error = data.activateAccount.errors.join(', ');
      } else {
        this.user = data.activateAccount.user;
        if (this.user) {
          await this.login(); // Wait for login to complete before redirecting
        }
      }
    } catch (error) {
      this.error = 'An error occurred while activating your account.';
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
