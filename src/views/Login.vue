<template>
  <div class="login-container">
    <div class="login">
      <h1>Login</h1>
      <div v-if="errors.length" class="error-message">
        <ul>
          <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
      </div>
      <Form @submit="login" v-slot="{ errors }" class="login-form">
        
        <div class="form-group">
          <label for="email">Email</label>
          <Field
            v-model="email"
            id="email"
            name="email"
            type="email"
            placeholder="Email"
            class="input-field"
            :rules="validateEmail"
          />
          <ErrorMessage name="email" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <Field
            v-model="password"
            id="password"
            name="password"
            type="password"
            placeholder="Password"
            class="input-field"
            :rules="validatePassword"
          />
          <ErrorMessage name="password" class="text-red-600 text-sm" />
        </div>
        
        <button type="submit" class="login-button">Login</button>
      </Form>

      <p class="mt-4 text-center text-sm text-black">
        Don't have an account?
        <router-link to="/signup" class="text-blue-500 hover:text-blue-800">Sign Up</router-link>
      </p>

      
    </div>
  </div>
</template>

<script>
import { Field, ErrorMessage, Form } from 'vee-validate';
import gql from 'graphql-tag';
import { useRoute, useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
  name: 'Login',
  components: {
    Field,
    ErrorMessage,
    Form,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const successMessage = ref(null);

    onMounted(() => {
      const initialSuccessMessage = route.query.successMessage;
      if (initialSuccessMessage) {
        successMessage.value = initialSuccessMessage; // Update reactive variable
        showSuccessToast(successMessage.value);
      }
    });

    const showSuccessToast = (message) => {
      toast.success(message); // Show success toast
      setTimeout(() => {
        router.replace({ ...route, query: {} }); // Delayed route replacement
      }, 2000); // Replace after 2 seconds (adjust delay as needed)
    };  

    return {
    };
  },
  data() {
    return {
      email: '',
      password: '',
      errors: [],
    };
  },
  methods: {
    async login() {
      // Clear previous errors
      this.errors = [];

      try {
    const { data } = await this.$apollo.mutate({
      mutation: gql`
        mutation LoginUser($email: String!, $password: String!) {
          loginUserMutation(input: {email: $email, password: $password}) {
            token
            user {
              id
              email
            }
            errors
          }
        }
      `,
      variables: {
        email: this.email,
        password: this.password,
      },
    });

    if (data.loginUserMutation.errors.length) {
      this.errors = data.loginUserMutation.errors;
      console.log(this.errors);
    } else {
      const token = data.loginUserMutation.token;
      const userId = data.loginUserMutation.user.id;
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
      console.log("IS ADMIN: ", isAdmin)
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
    this.errors.push('An error occurred while logging in.');
  }
    },
    async validateEmail(value) {
  if (!value) {
    return 'Email is required';
  }
  if (!/^[\w+\-.]+@[a-z\d\-.]+\.[a-z]+$/.test(value)) {
    return 'Invalid email format';
  }

  try {
    const { data, errors } = await this.$apollo.query({
      query: gql`
        query CheckEmailExistence($email: String!) {
          checkEmailExistence(email: $email) {
          id
          email
        }
        }
      `,
      variables: {
        email: value
      }
    });

    if (errors) {
      console.error('GraphQL Errors:', errors);
      return 'Error checking email existence';
    }

    if (!data.checkEmailExistence) {
      return 'Email does not exist';
    }

    return true;
  } catch (error) {
    console.error('Error:', error.message);
    return 'Error checking email existence'; // Handle unexpected errors
  }
},
validatePassword(value) {
  if (!value) {
    return 'Password is required';
  }
  if (value.length < 6) {
    return 'Password must be at least 6 characters';
  }
  // Add more complex password rules if needed
  return true;
}
  },
};
</script>


<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.login {
  max-width: 400px;
  width: 100%;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.login h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  display: grid;
  gap: 5px;
  margin-top: 5px;
  margin-bottom: 5px;
}

.input-field {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.login-button {
  background-color: #4b5563;
  color: #ffffff;
  border: none;
  padding: 12px 20px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 5px;
}

.login-button:hover {
  background-color: #6b7280;
}

.error-message {
  margin-top: 10px;
}

.error-message ul {
  list-style-type: none;
  padding: 0;
}

.error-message li {
  color: #ff0000;
  font-size: 14px;
  margin-bottom: 5px;
}
</style>
