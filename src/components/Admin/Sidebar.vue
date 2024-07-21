<template>
    <div class="bg-gray-800" :class="[sidebarBgColor, dataOpenSideBar ? 'side-bar-visible' : 'side-bar-close']" id="side-bar">
        <!-- Header Section -->
        <div :class="[sidebarHeaderBgColor, 'h-[64px] flex justify-center items-center']">
            <div class="text-2xl font-bold text-center flex items-center justify-center text-white h-full mt-6" v-show="dataOpenSideBar">
                <span class="font-weight-light">Chat</span>
                <span>Daters</span>
            </div>
            <img src="https://avatars.githubusercontent.com/u/97021587?v=4" v-show="!dataOpenSideBar" class="p-1 w-8 h-8 rounded-full ring-2 ring-gray-100 dark:ring-gray-500" alt="Avatar" />
        </div>
        <!-- Menu Section -->
        <div class="flex flex-col justify-between h-[calc(100vh-3rem)] bg-gray-900">
            <div class="menu-man text-left px-2 whitespace-nowrap">
                <!-- Profile Section -->
                <div class="profile flex justify-center items-center text-center p-5">
                    <div class="text-center text-white" v-show="dataOpenSideBar">
                        <img src="https://avatars.githubusercontent.com/u/97021587?v=4" class="p-1 w-24 h-24 rounded-full ring-2 ring-gray-300 dark:ring-gray-500 mb-4 mt-6 ml-4" alt="Avatar" />
                        <h5 class="text-xl font-medium leading-tight">Super Admin</h5>
                        <p class="text-gray-500">Admin</p>
                    </div>
                </div>
                <!-- Sidebar Links -->
                <div v-for="link in links" :key="link.name" :class="getLinkClass(link.route)" class="py-3 rounded-md cursor-pointer mb-2">
                    <router-link v-if="link.name !== 'Logout'" :to="link.route" class="px-2 flex space-x-2">
                        <span :class="iconClass(link.icon)"></span>
                        <span v-show="dataOpenSideBar">{{ link.name }}</span>
                    </router-link>
                    <button v-else @click="logout" class="px-2 flex space-x-2">
                        <span :class="iconClass(link.icon)"></span>
                        <span v-show="dataOpenSideBar">{{ link.name }}</span>
                    </button>
                    </div>
            </div>
        </div>
    </div>
</template>

<script>
import gql from 'graphql-tag';
export default {

    props: {
        dataOpenSideBar: Boolean
    },
    data() {
        return {
            links: [
                { name: 'Dashboard', route: '/admin', icon: 'pi-microsoft' },
                { name: 'Matches', route: '/admin/matches', icon: 'pi-users' },
                { name: 'Users', route: '/admin/users', icon: 'pi-user' },
                { name: 'Logout', route: '/', icon: 'pi-power-off' }
            ]
        };
    },
    methods: {
      isRouteActive(routePath) {
    const currentRoute = this.$route.path;
    // Dashboard should not be highlighted if on paths other than the root
    if (routePath === '/admin') {
      return currentRoute === '/admin';
    }

    // For other routes, highlight if they match the current route
    return currentRoute.startsWith(routePath) && (currentRoute === routePath || currentRoute.length > routePath.length);
  },
  getLinkClass(routePath) {
    // Exclude 'Logout' link from being checked for active state
    return routePath !== '/' && this.isRouteActive(routePath) ? 'bg-[#274654]' : 'hover:bg-[#637575]';
  },
        iconClass(iconName) {
            return `pi ${iconName} ${this.iconColor}`;
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
    },
    computed: {
        sidebarBgColor() {
            return 'bg-gray-900';
        },
        sidebarHeaderBgColor() {
            return 'bg-gray-900';
        },
        textColor() {
            return 'text-[#A4C2C9]'; // Adjust text color
        },
        iconColor() {
            return 'text-[#A4C2C9]'; // Adjust icon color
        }
    }
};
</script>

<style>
.p-tooltip-text {
  font-size: 10px !important;
}

#side-bar {
  overflow: hidden;
  transition: 300ms;
}

.side-bar-visible {
  width: 250px !important;
}

.side-bar-close {
  width: 50px !important;
}

/* Default text color for links */
.menu-man .cursor-pointer .px-2 {
  color: #A4C2C9; /* Adjusted text color */
}

/* Hover effect for links */
.menu-man .cursor-pointer .px-2:hover {
  color: #FFFFFF; /* text-white */
}

/* Ensure text and icon colors are correct for inactive routes */
.menu-man .cursor-pointer .px-2 .pi {
  color: #A4C2C9; /* Adjusted icon color */
}

/* Hover effect for icons */
.menu-man .cursor-pointer .px-2:hover .pi {
  color: #FFFFFF; /* text-white */
}
</style>
