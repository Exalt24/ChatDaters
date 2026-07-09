<template>
  <footer class="shadow-lg">
    <div class="max-w-6xl mx-auto px-4 py-10">
      <div class="xl:grid xl:grid-cols-2 xl:gap-8">
        <!-- About section -->
        <div class="space-y-6 xl:col-span-1 mr-10">
          <img src="/logo.png" alt="ChatDaters Logo" class="h-20 w-50">
          <!-- If you want the subheading text -->
          <p class="text-[#7d7d7d] leading-6">
            Connecting Hearts, One Swipe at a Time.
          </p>

          <div class="mt-6 flex">
            <a href="#" class="text-gray-400 hover:text-gray-100 p-2">
              <i class="pi pi-facebook h-6 w-6"></i>
            </a>
            <a href="#" class="text-gray-400 hover:text-gray-100 p-2">
              <i class="pi pi-twitter h-6 w-6"></i>
            </a>
            <a href="#" class="text-gray-400 hover:text-gray-100 p-2">
              <i class="pi pi-instagram h-6 w-6"></i>
            </a>
          </div>
        </div>

        <!-- Quick Links and Contact -->
        <div class="xl:col-span-1 xl:flex xl:justify-between">
          <!-- Quick Links -->
          <div class="mt-12 xl:mt-0">
            <h3 class="text-md font-semibold text-black tracking-wider uppercase">Quick Links</h3>
            <ul class="mt-4 space-y-4">
              <!-- Always display the Home link -->
              <li>
                <i class="pi pi-home text-[#7d7d7d]"></i>
                <router-link to="/" class="text-[#7d7d7d] leading-6"> Home</router-link>
              </li>

              <!-- Conditionally render these links based on currentUser -->
              <template v-if="currentUser">
                <li>
                  <i class="pi pi-user text-[#7d7d7d]"></i>
                  <router-link :to="`/${currentUser.id}/profile`" class="text-[#7d7d7d] leading-6"> Profile</router-link>
                </li>
                <li>
                  <i class="pi pi-heart text-[#7d7d7d]"></i>
                  <router-link :to="`/${currentUser.id}/matches`" class="text-[#7d7d7d] leading-6"> Matches</router-link>
                </li>
                <li>
                  <i class="pi pi-star text-[#7d7d7d]"></i>
                  <router-link :to="`/${currentUser.id}/swipe`" class="text-[#7d7d7d] leading-6"> Swipe</router-link>
                </li>
                <li>
                  <i class="pi pi-comments text-[#7d7d7d]"></i>
                  <router-link :to="`/${currentUser.id}/conversations`" class="text-[#7d7d7d] leading-6"> Conversations</router-link>
                </li>
              </template>
            </ul>
          </div>

          <!-- Contact information -->
          <div class="mt-12 xl:mt-0">
            <h3 class="text-md font-semibold tracking-wider uppercase text-black">Contact</h3>
            <ul class="mt-4 space-y-4">
              <li>
                <p class="text-[#7d7d7d] leading-6">123 Love Street <br>Romance City, RC 12345</p>
              </li>
              <li>
                <p class="text-[#7d7d7d] leading-6">Email: support@chatdaters.com</p>
              </li>
              <li>
                <p class="text-[#7d7d7d] leading-6">Phone: (123) 456-7890</p>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Copyright -->
    <div class="bg-black pt-4 pb-4 md:flex md:items-center md:justify-center">
      <p class="text-[#7d7d7d] leading-6 text-white md:order-1">
        &copy; {{ new Date().getFullYear() }} ChatDaters, Inc. All rights reserved.
      </p>
    </div>
  </footer>
</template>

<script>
import gql from 'graphql-tag';

export default {
  name: 'Footer',
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
    isAdminPage() {
      return this.$route.path.startsWith('/admin');
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
footer a:hover {
  color: #d1d5db; /* Slightly darker shade for hover effect */
}
</style>
