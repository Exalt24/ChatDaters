<template>
  <header class="bg-white shadow-lg">
    <div class="max-w-6xl mx-auto px-4 py-6 flex items-center justify-between">
      <!-- Logo and Navigation -->
      <div class="flex items-center">
        <router-link to="/">
          <img src="/logo.png" alt="ChatDaters Logo" class="h-12 w-50">
        </router-link>
        <nav class="ml-6 space-x-4">
          <!-- Always display the Home link -->
          <router-link 
            to="/" 
            :class="{'nav-link': true, 'active': isActive('/')}">
            <i class="pi pi-home"></i> Home
          </router-link>

          <!-- Conditionally render these links based on currentUser -->
          <template v-if="currentUser">
            <router-link 
              :to="`/${currentUser.id}/profile`" 
              :class="{'nav-link': true, 'active': isActive(`/${currentUser.id}/profile`)}">
              <i class="pi pi-user"></i> Profile
            </router-link>
            <router-link 
              :to="`/${currentUser.id}/matches`" 
              :class="{'nav-link': true, 'active': isActive(`/${currentUser.id}/matches`)}">
              <i class="pi pi-heart"></i> Matches
            </router-link>
            <router-link 
              :to="`/${currentUser.id}/swipe`" 
              :class="{'nav-link': true, 'active': isActive(`/${currentUser.id}/swipe`)}">
              <i class="pi pi-star"></i> Swipe
            </router-link>
            <router-link 
              :to="`/${currentUser.id}/conversations`" 
              :class="{'nav-link': true, 'active': isActive(`/${currentUser.id}/conversations`)}">
              <i class="pi pi-comments"></i> Conversations
            </router-link>
          </template>
        </nav>
      </div>

      <!-- Auth Buttons and Social Media Icons -->
      <div class="flex items-center space-x-4">
        <!-- Auth Buttons -->
        <div v-if="currentUser">
          <!-- Logged in view -->
          <button @click="logout" class="button-link">
            <i class="pi pi-sign-out"></i> Logout
          </button>
        </div>
        <div v-else>
          <!-- Not logged in view -->
          <router-link to="/signup" class="button-link mr-4">
            <i class="pi pi-user-plus"></i> Sign Up
          </router-link>
          <router-link to="/login" class="button-link">
            <i class="pi pi-sign-in"></i> Log In
          </router-link>
        </div>

        <!-- Social Media Icons -->
        <div class="flex items-center space-x-4">
          <a href="#" class="text-gray-500 hover:text-gray-800">
            <i class="pi pi-facebook h-6 w-6"></i>
          </a>
          <a href="#" class="text-gray-500 hover:text-gray-800">
            <i class="pi pi-twitter h-6 w-6"></i>
          </a>
          <a href="#" class="text-gray-500 hover:text-gray-800">
            <i class="pi pi-instagram h-6 w-6"></i>
          </a>
        </div>
      </div>
    </div>
  </header>
</template>


<script>
import gql from 'graphql-tag';

export default {
  name: 'Header',
  data() {
    return {
      currentUser: null,
      loading: true, // Add a loading state
    };
  },
  methods: {
    async fetchCurrentUser() {
      try {
        if (this.$apollo) {
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
        } else {
          console.log("Apollo is Busy");
        }
      } catch (error) {
        console.error('Fetch current user error:', error.message);
      } finally {
        this.loading = false; // Set loading to false after fetching data
      }
    },
    async logout() {
      if (confirm('Are you sure you want to logout?')) {
        try {
          await this.$apollo.mutate({
            mutation: gql`
              mutation LogoutUserMutation {
                logoutUserMutation(input: {}) {
                  success
                }
              }
            `
          });
          // Clear local storage and Apollo cache

          localStorage.removeItem('token');
          this.$apollo.getClient().resetStore(); // Clear the Apollo Client cache
          this.currentUser = null;
          this.$router.push({ 
            name: 'Login', 
            query: { successMessage: 'Successfully logged out' }
          });
        } catch (error) {
          console.error('Logout error:', error.message);
        }
      }
    },
    isAdminPage() {
      return this.$route.path.startsWith('/admin');
    },
    isActive(routePath) {
      const currentRoute = this.$route.path;
    // Dashboard should not be highlighted if on paths other than the root
    if (routePath === '/') {
      return currentRoute === '/';
    }

    // For other routes, highlight if they match the current route
    return currentRoute.startsWith(routePath) && (currentRoute === routePath || currentRoute.length > routePath.length);
    },
  },
  async created() {
    if (localStorage.getItem('token') && !this.isAdminPage()) {
      await this.fetchCurrentUser();
    }

    // Watch for route changes to fetch current user
    this.$watch('$route', async () => {
      if (!this.isAdminPage() && localStorage.getItem('token')) {
        await this.fetchCurrentUser();
      } else {
        this.currentUser = null;
      }
    });
  },
};
</script>

<style scoped>
header {
  z-index: 10; /* Ensures header stays above other content */
}
header a {
  transition: color 0.3s ease;
}
header a:hover {
  color: #4b5563; /* Darker shade for hover effect */
}

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

.nav-link {

  align-items: center;
  gap: 8px; /* Space between icon and text */
  text-decoration: none;
  color: #4b5563;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav-link:hover {
  background-color: gray; /* Change to your preferred hover background color */
  color: white; /* Change to your preferred hover text color */
}

.nav-link.active {
  background-color: #4b5563; /* Highlight background color */
  color: white; /* Highlight text color */
}
</style>
