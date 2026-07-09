<template>
    <div class="w-full max-w-6xl mx-auto mt-8">
  
      <h2 class="text-2xl text-gray-800 font-medium mt-8 mb-4">Stats</h2>
  
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
<!-- Users Card -->
<router-link :to="{ name: 'Users' }" class="max-w-sm rounded overflow-hidden shadow-xl bg-gradient-to-r from-gray-400 to-gray-300">
  <div class="flex justify-center items-center h-full">
    <div class="px-6 py-4 text-center">
      <div class="font-bold text-xl mb-2 text-white">Users</div>
      <p class="text-white text-base">
        {{ totalUsers }}
      </p>
    </div>
  </div>
</router-link>


        <router-link :to="{ name: 'Matches' }" class="max-w-sm rounded overflow-hidden shadow-xl bg-gradient-to-r from-gray-400 to-gray-300">
          <div class="flex justify-center items-center h-full">
            <div class="px-6 py-4 text-center">
              <div class="font-bold text-xl mb-2 text-white">Matches</div>
              <p class="text-white text-base">
                {{ totalMatches }}
              </p>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </template>
  
  <script>
  import gql from 'graphql-tag';
  import 'primeicons/primeicons.css';
  import Card from 'primevue/card';
  import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
  
  export default {
    name: 'Dashboard',
    components: {
      'p-card': Card,
    },
    data() {
      return {
        currentUser: null,
        totalUsers: 0,
        totalMatches: 0,
      };
    },
    methods: {
    fetchCurrentUser() {
      this.$apollo.query({
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
      })
      .then((response) => {
        console.log("Current U: ", response.data.currentUser)
        this.currentUser = response.data.currentUser;
      })
      .catch((error) => {
        console.error(error.message);
      });
    },
    showSuccessToast(message) {
      toast.success(message); // Show success toast
      setTimeout(() => {
        this.$router.replace({ ...this.$route, query: {} }); // Delayed route replacement
      }, 2000); // Replace after 2 seconds (adjust delay as needed)
    },
    
  },
    async mounted() {
      try {
        const { data } = await this.$apollo.query({
          query: gql`
            query {
              totalUsers
              totalMatches
            }
          `,
        });
  
        if (data) {
          this.totalUsers = data.totalUsers;
          this.totalMatches = data.totalMatches;
        }
        const route = this.$route;
    
  if (localStorage.getItem('token')) {
    this.fetchCurrentUser();
  }
    const initialSuccessMessage = route.query.successMessage;
    if (initialSuccessMessage) {
      this.showSuccessToast(initialSuccessMessage);
    }
      } catch (error) {
        console.error('Error fetching dashboard data:', error.message);
      }
    },
  };
  </script>
  
  <style scoped>
  /* Add any scoped styles specific to this component */
  </style>
  