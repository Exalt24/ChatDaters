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
      this.openSidebar = !this.openSidebar
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

    // Fetch current user on every route change
    this.$router.afterEach(() => {
      if (localStorage.getItem('token') && this.isAdminPage()) {
        this.fetchCurrentUser();
      } else {
        this.currentUser = null;
      }
    });
  }
}
</script>

<style scoped>
/* Fixed Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 250px; /* Adjust as needed */
  background-color: transparent; /* Adjust as needed */
  z-index: 1000; /* Ensure it is above other content */
}

/* Main content container */
.main-content {
  margin-left: 250px; /* Adjust according to the width of the sidebar */
  display: flex;
  flex-direction: column;
  height: auto;
  
}

/* Fixed Header */
.header {
  position: fixed;
  top: 0;
  left: 250px; /* Adjust according to the width of the sidebar */
  width: calc(100% - 280px); /* Full width minus sidebar width */
  background-color: transparent; /* Adjust as needed */
  z-index: 1000; /* Ensure it is above other content */
  margin: 1rem;
}

/* Content area */
.content {
  margin-top: 60px; /* Adjust based on the height of the header */
  height: calc(100vh - 60px); /* Full height minus header height */
  height: auto;
}
</style>
