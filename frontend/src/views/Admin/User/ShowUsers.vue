<template>
    <div class="flex flex-col w-full overflow-x-auto sm:mx-0.5 lg:mx-0.5 mt-4">
      <div class="py-2 inline-block min-w-full">
        <div class="overflow-x-auto">
          <form class="flex justify-center gap-4 mb-4 items-center w-full mt-4 flex-wrap">
  <div class="w-1/3">
    <label for="search-id" class="block text-sm font-medium text-gray-700">ID</label>
    <input v-model="search.id" type="number" id="search-id" class="mt-1 block w-full rounded-md border border-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-medium" min="1">
  </div>

  <div class="w-1/3">
    <label for="search-email" class="block text-sm font-medium text-gray-700">Email</label>
    <input v-model="search.email" type="text" id="search-email" class="mt-1 block w-full rounded-md border border-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-medium">
  </div>

  <div class="w-1/3">
    <label for="search-firstName" class="block text-sm font-medium text-gray-700">First Name</label>
    <input v-model="search.firstName" type="text" id="search-firstName" class="mt-1 block w-full rounded-md border border-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-medium">
  </div>

  <div class="w-1/3">
    <label for="search-lastName" class="block text-sm font-medium text-gray-700">Last Name</label>
    <input v-model="search.lastName" type="text" id="search-lastName" class="mt-1 block w-full rounded-md border border-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-medium">
  </div>

  <div class="w-1/3">
    <label for="search-created-at-from" class="block text-sm font-medium text-gray-700">Created At From</label>
    <input v-model="search.createdAtFrom" type="date" id="search-created-at-from" class="mt-1 block w-full rounded-md border border-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
  </div>

  <div class="w-1/3">
    <label for="search-created-at-to" class="block text-sm font-medium text-gray-700">Created At To</label>
    <input v-model="search.createdAtTo" type="date" id="search-created-at-to" class="mt-1 block w-full rounded-md border border-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
  </div>

  <div class="w-1/3 flex items-center justify-center">
    <button @click.prevent="clearFilter" type="button" v-if="hasFilters" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 cursor-pointer bg-[#e4ebe8] hover:bg-gray-100">Clear</button>
  </div>
</form>




          <!-- Users Table -->
          <table class="min-w-full table-fixed overflow-x-scroll">
            <thead class="bg-white border-b">
              <tr>
                <th scope="col" class="w-1/6 text-sm font-medium px-6 py-4">
                </th>
                <th scope="col" class="w-1/6 text-sm font-medium text-gray-800 px-6 py-4 text-left cursor-pointer" @click="sortBy('id')">
                  ID
                  <span v-if="sortOrder.column === 'id'" class="ml-1">
                    <svg v-if="sortOrder.order === 'asc'" class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 6.293a1 1 0 011.414 0L10 9.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 13.707a1 1 0 01-1.414 0L10 10.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </th>
                <th scope="col" class="w-1/8 text-sm font-medium text-gray-800 px-6 py-4 text-left cursor-pointer" @click="sortBy('email')">
                  Email
                  <span v-if="sortOrder.column === 'email'" class="ml-1">
                    <svg v-if="sortOrder.order === 'asc'" class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 6.293a1 1 0 011.414 0L10 9.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 13.707a1 1 0 01-1.414 0L10 10.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </th>
                <th scope="col" class="w-1/6 text-sm font-medium text-gray-800 px-6 py-4 text-left cursor-pointer" @click="sortBy('firstName')">
                  First Name
                  <span v-if="sortOrder.column === 'firstName'" class="ml-1">
                    <svg v-if="sortOrder.order === 'asc'" class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 6.293a1 1 0 011.414 0L10 9.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 13.707a1 1 0 01-1.414 0L10 10.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </th>
                <th scope="col" class="w-1/6 text-sm font-medium text-gray-800 px-6 py-4 text-left cursor-pointer" @click="sortBy('lastName')">
                  Last Name
                  <span v-if="sortOrder.column === 'lastName'" class="ml-1">
                    <svg v-if="sortOrder.order === 'asc'" class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 6.293a1 1 0 011.414 0L10 9.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 13.707a1 1 0 01-1.414 0L10 10.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </th>
                <th scope="col" class="w-5/6 text-sm font-medium text-gray-800 px-6 py-4 text-left cursor-pointer" @click="sortBy('createdAt')">
                  Created At
                  <span v-if="sortOrder.column === 'createdAt'" class="ml-1">
                    <svg v-if="sortOrder.order === 'asc'" class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 6.293a1 1 0 011.414 0L10 9.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 13.707a1 1 0 01-1.414 0L10 10.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </th>
                <th scope="col" class="w-1/16 text-sm font-medium text-gray-800 px-6 py-4 text-left">
                    Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in paginatedUsers" :key="user.id" class="bg-gray-50 border-b cursor-pointer hover:bg-[#637575]" @click="navigateToUser(user.id)">
                <td class="px-6 py-4 text-sm font-medium text-gray-800">
        <img v-if="user.images && user.images.length > 0" :src="user.images[0]" alt="User Photo" class="w-12 h-12 object-cover rounded-full">
        <img v-else src="/default-user.png" alt="Default Photo" class="w-12 h-12 object-cover rounded-full">
      </td>
                <td class="px-6 py-4 text-sm font-medium text-gray-800">{{ user.id }}</td>
                <td class="px-6 py-4 text-sm font-medium text-gray-800">{{ user.email }}</td>
                <td class="px-6 py-4 text-sm font-medium text-gray-800">{{ user.firstName }}</td>
                <td class="px-6 py-4 text-sm font-medium text-gray-800">{{ user.lastName }}</td>
                <td class="px-6 py-4 text-sm font-medium text-gray-800">{{ formattedCreatedAt(user.createdAt) }}</td>
                <td class="px-6 py-4 text-sm font-medium text-gray-800 relative z-99999">
                <div class="flex justify-center items-center">
                  <button @click.stop="toggleActions(user.id)" class="rounded-full focus:outline-none focus:ring-0 focus:ring-blue-500 flex items-center mt-2">
                    <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M10 6a2 2 0 100-4 2 2 0 000 4zM2 6a2 2 0 100-4 2 2 0 000 4zm16 0a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                    </svg>
                  </button>
                  <div v-if="activeActions === user.id" class="absolute bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 mt-2 right-0 left-1 top-8 z-10">
                    <button @click.stop="navigateToUser(user.id)" class="block text-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full" role="menuitem">View</button>
                    <button @click.stop="navigateToUserEdit(user.id)" class="block text-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full" role="menuitem">Edit</button>
                    <button @click.stop="deleteUser(user.id)" class="block text-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full" role="menuitem">Delete</button>
                  </div>
                </div>
              </td>
              </tr>
              <!-- Placeholder for loading or no data message -->
              <tr v-if="loading">
              <td colspan="6" class="px-6 py-4 text-sm font-medium text-gray-800 text-center">Loading...</td>
            </tr> 
            <tr v-else-if="dateRangeNotice != ''">
              <td colspan="6" class="px-6 py-4 text-sm font-medium text-red-400 text-center">{{ dateRangeNotice }}</td>
            </tr>
            <tr v-else-if="paginatedUsers.length === 0">
              <td colspan="6" class="px-6 py-4 text-sm font-medium text-gray-800 text-center">No users found.</td>
            </tr>
            </tbody>
          </table>
          <div class="flex justify-center items-center mt-4">
            <!-- Pagination component -->
            <Paginator
              v-model:first="first"
              :totalRecords="totalUsers"
              :rows="perPage"
              @page-change="handlePageChange"
              :template="{
                '640px': 'PrevPageLink CurrentPageReport NextPageLink',
                '960px': 'FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink',
                '1300px': 'FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink',
                default: 'FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink JumpToPageDropdown JumpToPageInput'
              }"
            />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Paginator from 'primevue/paginator';
  import gql from 'graphql-tag';
  import { useRoute, useRouter } from 'vue-router';
  import { onMounted, ref } from 'vue';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
  

  export default {
    name: 'ShowUsers',
    components: {
      Paginator,
    },

    setup() {
      const router = useRouter();
    const route = useRoute();

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
        users: [],
        first: 0,
        perPage: 10,
        loading: false,
        activeActions: null, // Track which user's actions menu is active
      search: {
        id: '',
        email: '',
        firstName: '',
        lastName: '',
      },
        sortOrder: {
          column: 'id',  // Initial column to sort by (e.g., ID)
          order: 'asc',
        },
      };
    },
    computed: {
      paginatedUsers() {
        const startIndex = this.first;
        const endIndex = startIndex + this.perPage;
        return this.sortedUsers.slice(startIndex, endIndex);
      },
      totalUsers() {
        return this.sortedUsers.length;
      },
      hasFilters() {
      return (
        this.search.id ||
        this.search.email ||
        this.search.firstName ||
        this.search.lastName ||
        this.search.createdAtFrom ||
        this.search.createdAtTo
      );
    },
      sortedUsers() {
        let sorted = [...this.filteredUsers];
  
        if (this.sortOrder.column && this.sortOrder.order) {
          sorted = sorted.sort((a, b) => {
            const modifier = this.sortOrder.order === 'desc' ? -1 : 1;
  
            if (this.sortOrder.column === 'createdAt') {
              const dateA = new Date(a.createdAt);
              const dateB = new Date(b.createdAt);
              return (dateA - dateB) * modifier;
            } else if (this.sortOrder.column === 'id') {
              return (parseInt(a.id) - parseInt(b.id)) * modifier;
            } else {
              const aValue = a[this.sortOrder.column].toString().toLowerCase();
              const bValue = b[this.sortOrder.column].toString().toLowerCase();
              if (aValue < bValue) return -1 * modifier;
              if (aValue > bValue) return 1 * modifier;
              return 0;
            }
          });
        }
  
        return sorted;
      },
      filteredUsers() {
  let filtered = [...this.users];

  // Filter by ID
  if (this.search.id !== '') {
    filtered = filtered.filter(user => user.id.toString().startsWith(this.search.id.toString()));
  }

  // Filter by User ID
  if (this.search.email !== '') {
    filtered = filtered.filter(user => user.email.toLowerCase().toString().startsWith(this.search.email.toString()));
  }

  if (this.search.firstName !== '') {
    filtered = filtered.filter(user => user.firstName.toLowerCase().toString().startsWith(this.search.firstName.toString()));
  }

  if (this.search.lastName !== '') {
    filtered = filtered.filter(user => user.lastName.toLowerCase().toString().startsWith(this.search.lastName.toString()));
  }

  if (this.search.createdAtFrom && this.search.createdAtTo) {
    const startDate = new Date(this.search.createdAtFrom);
    const endDate = new Date(this.search.createdAtTo);

    const startDateUTC = Date.UTC(startDate.getFullYear(), startDate.getMonth(), startDate.getDate());
    const endDateUTC = Date.UTC(endDate.getFullYear(), endDate.getMonth(), endDate.getDate());

    endDate.setUTCHours(23, 59, 59, 999);

    filtered = filtered.filter(user => {
      const userDate = new Date(user.createdAt);

      const userDateUTC = Date.UTC(userDate.getFullYear(), userDate.getMonth(), userDate.getDate());

      return userDateUTC >= startDateUTC && userDateUTC <= endDateUTC;
    });
  }

  return filtered;
},
      formattedCreatedAt() {
      return function(createdAt) {
        if (!createdAt) return ''; // Handle empty or null values

        // Format createdAt using Date object
        const dateObj = new Date(createdAt);
        return dateObj.toLocaleString(); // Use toLocaleString for a localized date format
      };
    },
    dateRangeNotice() {
    if (this.search.createdAtFrom && this.search.createdAtTo) {
      const startDate = new Date(this.search.createdAtFrom);
      const endDate = new Date(this.search.createdAtTo);

      if (startDate > endDate) {
        return 'Start date cannot be after end date.';
      }
    }
    return '';
  },    
    },
    methods: {
        toggleActions(userId) {
      this.activeActions = this.activeActions === userId ? null : userId;
    },
    async deleteUser(userId) {
  if (confirm('Are you sure you want to delete this user?')) {
    try {
      await this.$apollo.mutate({
        mutation: gql`
          mutation DeleteUser($id: ID!) {
            deleteUserMutation(input: { id: $id }) {
              user {
                id
                email
                createdAt
              }
              errors
            }
          }
        `,
        variables: {
          id: userId,
        },
        update: (cache, { data: { deleteUserMutation } }) => {
          const { errors } = deleteUserMutation;

          if (errors && errors.length > 0) {
            throw new Error(errors.join(', '));
          }

          // Update users cache
          const usersQuery = gql`
            query GetUsers {
              users {
                id
                email
                firstName
                lastName
                admin
                createdAt
                images
                matches {
                  id
                  status
                }
              }
            }
          `;

          const existingData = cache.readQuery({ query: usersQuery });

          if (existingData) {
            const updatedUsers = existingData.users
              .filter(u => u.id !== userId) // Remove deleted user
              .map(u => {
                // Recalculate matchedCount
                const matchedCount = u.matches.filter(match => match.status === "matched").length;
                return { ...u, matchedCount };
              });

            cache.writeQuery({
              query: usersQuery,
              data: {
                users: updatedUsers
              }
            });
          }

          // Update matches cache
          const matchesQuery = gql`
            query GetMatches {
              matches {
                id
                users {
                  id
                  firstName
                  lastName
                  images
                  locationCountry
                  locationRegion
                  locationCity
                  bio
                }
                status
                updatedAt
              }
            }
          `
          ;
          

          const existingMatches = cache.readQuery({ query: matchesQuery });

          if (existingMatches) {
            const updatedMatches = existingMatches.matches.map(match => ({
              ...match,
              users: match.users.filter(u => u.id !== userId)
            }));

            cache.writeQuery({
              query: matchesQuery,
              data: {
                matches: updatedMatches
              }
            });
          }
        }
      });

      // Refetch queries manually
      if (this.$apollo.queries.GetUsers) {
        this.$apollo.queries.GetUsers.refetch();
      }

      if (this.$apollo.queries.GetMatches) {
        this.$apollo.queries.GetMatches.refetch();
      }

      this.fetchUsers();
      toast.success("Successfully deleted the user");
    } catch (error) {
      console.error('Error deleting user:', error.message);
      toast.error(`Failed to delete user: ${error.message}`);
    }
  }
},
      fetchUsers() {
        this.loading = true;
        this.$apollo
          .query({
            query: gql`
              query GetUsers {
                users {
                  id
                  email
                  firstName
                  lastName
                  admin
                  createdAt
                  images
                  matches {
                  id
                  users {
                    id
                    firstName
                    lastName
                    images
                    locationCountry
                    locationRegion
                    locationCity
                    bio
                  }
                  status
                  updatedAt
                }
                }
              }
            `,
            fetchPolicy: 'network-only',
          })
          .then((response) => {
            const users = response.data.users;
            this.users = users.filter(user => !user.admin)
          })
          .catch((error) => {
            console.error(error.message);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      navigateToUser(userId) {
      this.$router.push({ name: 'Show User', params: { id: userId } });
    },
    navigateToUserEdit(userId) {
      this.$router.push({ name: 'Edit User', params: { id: userId } });
    },
      handlePageChange(event) {
        this.first = event.page * this.perPage;
      },
      clearFilter() {
      this.search.id = '';
      this.search.email = '';
      this.search.firstName = '';
      this.search.lastName = '';
      this.search.createdAtFrom = '';
      this.search.createdAtTo = '';
    },
      sortBy(column) {
        if (this.sortOrder.column === column) {
          this.sortOrder.order = this.sortOrder.order === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortOrder.column = column;
          this.sortOrder.order = 'asc';
        }
      },
    },
    
    mounted() {
      this.fetchUsers();
    },
  };
  </script>
  
  <style scoped>
  /* Add any custom styles here */
  </style>
  