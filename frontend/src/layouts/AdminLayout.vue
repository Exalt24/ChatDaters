<template>
  <div class="flex min-h-screen">
    <sidebar class="sidebar" :dataOpenSideBar="openSidebar" />
    <div class="main-content flex-1">
      <headerTop class="header" :dataOpenSideBar="openSidebar" :clickHamburger="toggleSidebar" />
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderTop from './../components/Admin/Header.vue'
import Sidebar from './../components/Admin/Sidebar.vue'
import gql from 'graphql-tag';

export default {
  components: {
    HeaderTop,
    Sidebar
  },
  data() {
    return {
      currentUser: null,
      openSidebar: true
    }
  },
  methods: {
    toggleSidebar() {
      this.openSidebar = !this.openSidebar;
      // Dynamically set the CSS variable based on sidebar state
      document.documentElement.style.setProperty('--sidebar-width', this.openSidebar ? '250px' : '80px');
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
        if (this.currentUser && !this.currentUser.admin) {
          this.$router.push({ 
            name: 'Home', 
            query: { errorMessage: 'Unauthorized Access' }
          });
        }
      } catch (error) {
        console.error('Fetch current user error:', error.message);
        this.$router.push({ 
          name: 'Home', 
          query: { errorMessage: 'Unauthorized Access' }
        });
      }
    },
    isAdminPage() {
      return this.$route.path.startsWith('/admin');
    },
  },

  async mounted() {
    if (localStorage.getItem('token')) {
      await this.fetchCurrentUser();
    } else {
      this.$router.push({ 
        name: 'Home', 
        query: { errorMessage: 'Unauthorized Access' }
      });
    }
    // Set initial CSS variable
    document.documentElement.style.setProperty('--sidebar-width', this.openSidebar ? '250px' : '80px');
  }
}
</script>

<style scoped>
/* Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: var(--sidebar-width, 250px); /* Use CSS variable for dynamic width */
  background-color: transparent; /* Adjust as needed */
  z-index: 1000; /* Ensure it is above other content */
  transition: width 0.3s; /* Smooth transition for sidebar width */
}

/* Main content container */
.main-content {
  margin-left: var(--sidebar-width, 250px); /* Use CSS variable for dynamic margin */
  display: flex;
  flex-direction: column;
  height: auto;
  transition: margin-left 0.3s; /* Smooth transition for content margin */
}

/* Header */
.header {
  position: fixed;
  top: 0;
  left: var(--sidebar-width, 250px); /* Use CSS variable for dynamic left position */
  width: calc(100% - var(--sidebar-width, 250px) - 30px); /* Adjust for header margin */
  background-color: transparent; /* Adjust as needed */
  z-index: 1000; /* Ensure it is above other content */
  margin: 1rem;
  transition: left 0.3s; /* Smooth transition for header position */
}

/* Content area */
.content {
  margin-top: 60px; /* Adjust based on the height of the header */
  height: calc(100vh - 60px); /* Full height minus header height */
  height: auto;
}
</style>
