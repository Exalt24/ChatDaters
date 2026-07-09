<template>
  <div class="max-w-6xl mx-auto mt-8 mb-8">
    <div v-if="user" :id="`user-${user.id}`" class="grid grid-cols-2 gap-8">
      <div>
        <div class="rounded-md p-3 bg-gray-200">
        <Galleria
      :value="galleriaImages"
      :numVisible="5"
      :pt="ptOptions"
      :showThumbnailNavigators="false"
      :showItemNavigators="true"
    >
    <template #item="slotProps">
        <img
          :src="slotProps.item.itemImageSrc"
          :alt="'Image'"
          style="width: 550px; height: 350px; object-fit: cover; display: block;"
        />
      </template>
      <template #thumbnail="slotProps">
        <img
          :src="slotProps.item.thumbnailImageSrc"
          :alt="'Thumbnail'"
          style="width: 50px; height: 50px; object-fit: cover; display: block;"
        />
      </template>
    </Galleria>
    <div class="my-5">
      <strong class="block text-center" :style="{ fontSize: '20px' }">{{ user.firstName }} {{ user.lastName }}</strong>
        </div>
        <div class="my-5">
          <strong class="block font-medium mb-1">Location:</strong>
          <p>{{ user.locationCountry }}, {{ user.locationRegion }}, {{ user.locationCity }}</p>
        </div>
        <div class="my-5">
          <strong class="block font-medium mb-1">Bio:</strong>
          <p>{{ user.bio }}</p>
        </div>
  </div>  

      </div>

      <div class="rounded-lg p-3 bg-gray-200">
  <strong class="block" :style="{ fontSize: '30px' }">Additional Details:</strong>
  <!-- User Additional Details -->
  <div class="my-5">
    <table class="min-w-full bg-white divide-y divide-gray-300">
      <tbody class="bg-white divide-y divide-gray-200">
        <tr>
          <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">ID:</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ user.id }}</td>
        </tr>
        <tr>
          <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Email:</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ user.email }}</td>
        </tr>
        <tr>
          <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Mobile Number:</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ user.mobileNumber }}</td>
        </tr>
        <tr>
          <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Birthdate:</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ formatDate(user.birthdate) }}</td>
        </tr>
        <tr>
          <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Gender:</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ user.gender }}</td>
        </tr>
        <tr>
          <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Sexual Orientation:</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ user.sexualOrientation }}</td>
        </tr>
        <tr>
          <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Gender Interest:</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ user.genderInterest }}</td>
        </tr>
        <tr>
          <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">School:</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ user.school || 'N/A' }}</td>
        </tr>
        <tr>
          <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Created At:</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ formattedCreatedAt(user.createdAt) }}</td>
        </tr>
        <tr>
          <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Updated At:</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ formattedCreatedAt(user.updatedAt) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

  
      <!-- User Matches -->
      <div class="col-span-3 mt-4 rounded-md p-3 bg-gray-200">
        <strong class="block" :style="{ fontSize: '30px' }">Matches:</strong>
        <table class="min-w-full bg-white divide-y divide-gray-300">
      <thead>
        <tr>
          <th class="px-4 py-2">ID</th>
          <th class="px-4 py-2">Name</th>
          <th class="px-4 py-2">View</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="match in paginatedMatches" :key="match.id" class="text-center">
          <td class="border px-4 py-2">{{ match.id }}</td>
          <td class="border px-4 py-2">{{ match.firstName }} {{ match.lastName }}</td>
          <td class="border px-4 py-2">
            <router-link :to="{ name: 'Show User', params: { id: match.id } }" class="inline-block">
              <svg class="w-8 h-8 text-gray-600 hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12m-3 3a3 3 0 110-6 3 3 0 010 6zm-6.293-3A8.973 8.973 0 0112 6a8.973 8.973 0 016.293 3A8.973 8.973 0 0112 18a8.973 8.973 0 01-6.293-3z"></path>
              </svg>
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="flex justify-center items-center mt-4">
            <!-- Pagination component -->
            <Paginator
              v-model:first="first"
              :totalRecords="totalMatches"
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
  
    <!-- Loading State -->
    <div v-else class="max-w-md mx-auto mt-8">
      Loading user...
    </div>
  
    <!-- Action Buttons -->
    <div v-if="user" class="max-w-6xl mx-auto mt-4 flex justify-between">
      <button @click="goBack" type="button" class="px-4 py-2 bg-gray-300 text-gray-900 rounded-md hover:bg-[#637575]">Back to Users</button>
      <div class="flex">
        <button @click="navigateToUserEdit(user.id)" class="px-4 py-2 bg-gray-200 text-gray-900 rounded-md hover:bg-[#637575]">Edit</button>
        <div class="ml-2">
          <button @click="deleteUser(user.id)" class="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-[#637575]">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import gql from 'graphql-tag';
  import { useRoute, useRouter } from 'vue-router';
  import { onMounted, ref } from 'vue';
  import { toast } from 'vue3-toastify';
  import 'vue3-toastify/dist/index.css';
  import Galleria from 'primevue/galleria';
  import Paginator from 'primevue/paginator';

  
  export default {
    name: 'ShowUser',
    components: {
      Galleria,
      Paginator
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
        user: null,
        defaultImage: '/default-user.png', // Path to your default image
        numberOfImages: 5,
        first: 0,
      perPage: 5,
      matches: [],
        ptOptions: {
          thumbnailContainer:{
          style:{
            backgroundColor: '#D1D5DB'
          }
        },
        thumbnailItem:{
          style: {
            padding: '5px'
          }
        },
          nextThumbnailButton:{
            style: {
            color: '#111827'
          }

          },
          previousThumbnailButton:{
            style: {
            color: '#111827'
          }
          },
      }
      };
    },
  
    computed: {
      formattedCreatedAt() {
        return function(createdAt) {
          if (!createdAt) return ''; // Handle empty or null values
  
          // Format createdAt using Date object
          const dateObj = new Date(createdAt);
          return dateObj.toLocaleString(); // Use toLocaleString for a localized date format
        };
      },
      galleriaImages() {
      const images = this.user.images || [];
      // Fill the array with default images if necessary
      const filledImages = [...images];
      while (filledImages.length < this.numberOfImages) {
        filledImages.push(this.defaultImage);
      }
      return filledImages.map(url => ({ itemImageSrc: url, thumbnailImageSrc: url }));
    },
    paginatedMatches() {
        const startIndex = this.first;
        const endIndex = startIndex + this.perPage;
        return this.matches.slice(startIndex, endIndex);
      },
      totalMatches() {
        return this.matches.length;
      },
    },
  
    apollo: {
      user: {
        query: gql`
          query User($id: ID!) {
            user(id: $id) {
              id
              firstName
              lastName
              mobileNumber
              locationCountry
              locationRegion
              locationCity
              images
              bio
              email
              createdAt
              updatedAt
              school
              birthdate
              gender
              sexualOrientation
              genderInterest
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
        variables() {
          return {
            id: this.$route.params.id
          };
        },
        update(data) {
          this.user = data.user;
          this.matches = data.user.matches
        .filter(match => match.status === "matched")
        .map(match => match.users.find(user => user.id !== this.user.id));
      console.log(this.matches);
          return data.user;
        },
        error(error) {
          console.error('Error fetching user:', error.message);
        }
      }
    },
    mounted() {
    console.log('Component mounted. User:', this.user); // Log user data when component is mounted
  },
    methods: {
      formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', { dateStyle: 'long' }).format(date);
  },
      deleteUser(userId) {
        if (confirm('Are you sure you want to delete this user?')) {
          this.$apollo.mutate({
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
            const { users } = cache.readQuery({ query: gql`{ users { id email createdAt admin } }` });
          const updatedUsers = users.filter(user => user.id !== userId);
          cache.writeQuery({ query: gql`{ users { id email createdAt admin } }`, data: { users: updatedUsers } });
        },
          }).then(() => {
            this.$router.push({ 
                name: 'Users', 
                query: { successMessage: 'Successfully deleted a user' }
            });
          }).catch(error => {
            console.error('Error deleting user:', error.message);
          });
        }
      },
      goBack() {
        this.$router.push({ name: 'Users' });
      },
      navigateToUserEdit(userId) {
      this.$router.push({ name: 'Edit User', params: { id: userId } });
    },
    handlePageChange(event) {
        this.first = event.page * this.perPage;
      },
    }
  };
  </script>
  
  <style scoped>
  </style>
  