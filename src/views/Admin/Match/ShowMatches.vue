<template>
  <div class="flex flex-col w-full overflow-x-auto sm:mx-0.5 lg:mx-0.5 mt-4">
    <div class="py-2 inline-block min-w-full">
      <div class="overflow-x-auto">

        <div class="flex justify-center">
  <form class="flex gap-4 mb-4 items-center mt-4 w-full max-w-4xl">
    <div class="flex-1 min-w-[200px]">
      <label for="search-id" class="block text-sm font-medium text-gray-700">ID</label>
      <input v-model="search.id" type="number" id="search-id" class="mt-1 block w-full rounded-md border border-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-medium" min="1">
    </div>

    <div class="flex-1 min-w-[200px]">
      <label for="search-name" class="block text-sm font-medium text-gray-700">Name</label>
      <input v-model="search.name" type="text" id="search-name" class="mt-1 block w-full rounded-md border border-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-medium">
    </div>

    <div class="flex-1 min-w-[200px]">
      <label for="search-number" class="block text-sm font-medium text-gray-700">No. of Matches</label>
      <input v-model="search.number" type="number" id="search-number" class="mt-1 block w-full rounded-md border border-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-medium" min="0">
    </div>

    <div class="flex-none">
      <button @click.prevent="clearFilter" type="button" v-if="hasFilters" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 cursor-pointer bg-[#e4ebe8] hover:bg-gray-100">Clear</button>
    </div>
  </form>
</div>

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
                <th scope="col" class="w-1/8 text-sm font-medium text-gray-800 px-6 py-4 text-left cursor-pointer" @click="sortBy('name')">
                  Name
                  <span v-if="sortOrder.column === 'name'" class="ml-1">
                    <svg v-if="sortOrder.order === 'asc'" class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 6.293a1 1 0 011.414 0L10 9.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 13.707a1 1 0 01-1.414 0L10 10.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </th>
                <th scope="col" class="w-1/6 text-sm font-medium text-gray-800 px-6 py-4 text-left cursor-pointer" @click="sortBy('number')">
                  No. of Matches
                  <span v-if="sortOrder.column === 'number'" class="ml-1">
                    <svg v-if="sortOrder.order === 'asc'" class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.293 6.293a1 1 0 011.414 0L10 9.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="h-4 w-4 inline-block text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M14.707 13.707a1 1 0 01-1.414 0L10 10.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                  </span>
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
                <td class="px-6 py-4 text-sm font-medium text-gray-800">{{ user.firstName }} {{ user.lastName }}</td>
                <td class="px-6 py-4 text-sm font-medium text-gray-800">{{ user.matchedCount }}</td>
                
              </tr>
              <!-- Placeholder for loading or no data message -->
              <tr v-if="loading">
              <td colspan="6" class="px-6 py-4 text-sm font-medium text-gray-800 text-center">Loading...</td>
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

  export default {
    name: 'ShowUsers',
    components: {
      Paginator,
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
        name: '',
        number: ''
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
        this.search.name ||
        this.search.number
      );
    },
      sortedUsers() {
        let sorted = [...this.filteredUsers];

        if (this.sortOrder.column && this.sortOrder.order) {
          sorted = sorted.sort((a, b) => {
            const modifier = this.sortOrder.order === 'desc' ? -1 : 1;
  
            if (this.sortOrder.column === 'number') {
        return (a.matchedCount - b.matchedCount) * modifier;
      } else if (this.sortOrder.column === 'id') {
        return (parseInt(a.id) - parseInt(b.id)) * modifier;
      } else if (this.sortOrder.column === 'name') {
        const aValue = `${a.firstName} ${a.lastName}`.toLowerCase();
        const bValue = `${b.firstName} ${b.lastName}`.toLowerCase();
        if (aValue < bValue) return -1 * modifier;
        if (aValue > bValue) return 1 * modifier;
        return 0;
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
  if (this.search.name !== '') {
  filtered = filtered.filter(user => {
    const fullName = `${user.firstName} ${user.lastName}`.toLowerCase();
    return fullName.startsWith(this.search.name.toLowerCase());
  });
}

  if (this.search.number !== '') {
    filtered = filtered.filter(user => user.matchedCount.toString().startsWith(this.search.number.toString()));
  }

  return filtered;
}
    },
    methods: {
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
                  matches{
                    id
                    status
                  }
                }
              }
            `,
          })
          .then((response) => {
            const users = response.data.users;
            this.users = users
        .filter(user => !user.admin)
        .map(user => {
          const matchedCount = user.matches.filter(match => match.status === "matched").length;
          return { ...user, matchedCount };
        });
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
    handlePageChange(event) {
        this.first = event.page * this.perPage;
      },
      clearFilter() {
      this.search.id = '';
      this.search.name = '';
      this.search.number = '';
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
    
    }
</script>

<style scoped>
</style>