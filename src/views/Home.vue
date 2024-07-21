<template>
  <div class="max-w-6xl mx-auto mt-8 mb-8 text-center" v-if="loading">Loading...</div>
    <div v-else>
    <!-- Hero Section -->
    <section class="bg-gray-100 py-20">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
            Find Your Match
          </h1>
          <p class="mt-4 text-lg leading-6 text-gray-700">
            Chat with people who share your interests.
          </p>
          <!-- Call to Action Buttons -->
          <div class="mt-10">
            <div v-if="currentUser">
              <!-- Logged in view -->
              <router-link :to="`/${currentUser.id}/swipe`" class="button-link">
              Swipe
            </router-link>
            </div>
            <div v-else>
              <!-- Not logged in view -->
              <router-link to="/signup" class="button-link mr-4">
                Sign Up
              </router-link>
              <router-link to="/login" class="button-link">
                Log In
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Profiles Section -->
    <section class="py-20">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-extrabold text-gray-900">Featured Profiles</h2>
        <div class="mt-12 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          <!-- Dynamic Profile Cards -->
          <div v-for="(profile, index) in featuredProfiles" :key="index" class="bg-white shadow-xl rounded-lg overflow-hidden">
            <img :src="profile.image" :alt="profile.name" class="w-full h-48 object-cover object-center">
            <div class="p-6">
              <h3 class="text-lg font-semibold text-gray-900">{{ profile.name }}</h3>
              <p class="mt-2 text-sm text-gray-600">{{ profile.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'Home',
  data() {
    return {
      currentUser: null,
      featuredProfiles: [], // Initialize as an empty array
      loading: true
    };
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      try {
        const response = await this.$apollo.query({
          query: gql`
            query GetUsers {
              users {
                id
                firstName
                lastName
                bio
                images
                admin
              }
            }
          `,
        });

        const users = response.data.users;
        let nonAdminUsers;
        if (this.currentUser) {
        nonAdminUsers = users
          .filter(user => !user.admin && user.id !== this.currentUser.id) // Filter out admin users and current user
          .map(user => ({
            name: `${user.firstName} ${user.lastName}` || "N/A",
            image: user.images[0] || "/default-user.png", // Use a default image if none available
            description: user.bio || "N/A"
          }));
        } else {
          nonAdminUsers = users
          .filter(user => !user.admin) // Filter out admin users and current user
          .map(user => ({
            name: `${user.firstName} ${user.lastName}` || "N/A",
            image: user.images[0] || "/default-user.png", // Use a default image if none available
            description: user.bio || "N/A"
          }));
        }
        // Shuffle the array and pick the first 3 profiles
        const shuffledUsers = nonAdminUsers.sort(() => 0.5 - Math.random());
        this.featuredProfiles = shuffledUsers.slice(0, 3);
      } catch (error) {
        console.error('Error fetching users:', error.message);
      } finally {
        this.loading = false;
      }
    },
    async fetchCurrentUser() {
      try {
        const response = await this.$apollo.query({
          query: gql`
            query GetCurrentUserData {
              currentUser {
                id
                email
                createdAt
                admin
              }
            }
          `,
        });
        this.currentUser = response.data.currentUser;
      } catch (error) {
        console.error('Error fetching current user:', error.message);
      }
    },
    showSuccessToast(message) {
      toast.success(message); // Show success toast
      setTimeout(() => {
        this.$router.replace({ ...this.$route, query: {} }); // Delayed route replacement
      }, 2000); // Replace after 2 seconds (adjust delay as needed)
    },
    showErrorToast(message) {
      toast.error(message); // Show error toast
      setTimeout(() => {
        this.$router.replace({ ...this.$route, query: {} }); // Delayed route replacement
      }, 2000); // Replace after 2 seconds (adjust delay as needed)
    },
    isAdminPage() {
      return this.$route.path.startsWith('/admin');
    },
  },
  async created() {

    const route = useRoute();

    if (localStorage.getItem('token') && !this.isAdminPage()) {
      await this.fetchCurrentUser();
    }

    await this.fetchUsers();

    // Watch for route changes to fetch current user
    this.$watch('$route', async () => {
      if (!this.isAdminPage() && localStorage.getItem('token')) {
        await this.fetchCurrentUser();
      } else {
        this.currentUser = null;
        this.users = null;
      }
    });

    
    const initialSuccessMessage = route.query.successMessage;
    if (initialSuccessMessage) {
      this.showSuccessToast(initialSuccessMessage);
    }

    const initialErrorMessage = route.query.errorMessage;
    if (initialErrorMessage) {
      this.showErrorToast(initialErrorMessage);
    }
  },
};
</script>

<style scoped>
.button-link {
  text-decoration: none;
  color: #4b5563; /* Default text color */
  background-color: transparent;
  border: 1px solid #4b5563;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.button-link:hover {
  background-color: #4b5563; /* Darker background on hover */
  color: white; /* Text color on hover */
}
</style>
