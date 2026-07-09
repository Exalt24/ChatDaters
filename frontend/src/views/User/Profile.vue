<template>
  <div class="max-w-6xl mx-auto mt-8 mb-8">
    <div v-if="user" :id="`user-${user.id}`">
      <!-- User Information Section -->
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
                class="galleria-item"
              />
            </template>
            <template #thumbnail="slotProps">
              <img
                :src="slotProps.item.thumbnailImageSrc"
                :alt="'Thumbnail'"
                class="galleria-thumbnail"
              />
            </template>
          </Galleria>
          <div class="flex justify-center gap-20 mt-4">
            <div>
              <strong class="block text-center user-name">{{ user.firstName }} {{ user.lastName }}</strong>
            </div>
          </div>
        </div>
      </div>
      
      <!-- User Additional Details Section -->
      <div class="rounded-lg p-3 bg-gray-200 mt-4">
        <strong class="block text-center details-title">Details:</strong>
        <div class="my-5">
          <table class="min-w-full bg-white divide-y divide-gray-300">
            <tbody class="bg-white divide-y divide-gray-200">
              <tr>
                <td class="px-6 py-4 font-medium text-gray-900">Location:</td>
                <td class="px-6 py-4">{{ user.locationCountry }}, {{ user.locationRegion }}, {{ user.locationCity }}</td>
              </tr>
              <tr>
                <td class="px-6 py-4 font-medium text-gray-900">Bio:</td>
                <td class="px-6 py-4">{{ user.bio }}</td>
              </tr>
              <tr>
                <td class="px-6 py-4 font-medium text-gray-900">Birthdate:</td>
                <td class="px-6 py-4">{{ formatDate(user.birthdate) }}</td>
              </tr>
              <tr>
                <td class="px-6 py-4 font-medium text-gray-900">Gender:</td>
                <td class="px-6 py-4">{{ user.gender }}</td>
              </tr>
              <tr>
                <td class="px-6 py-4 font-medium text-gray-900">Sexual Orientation:</td>
                <td class="px-6 py-4">{{ user.sexualOrientation }}</td>
              </tr>
              <tr>
                <td class="px-6 py-4 font-medium text-gray-900">Gender Interest:</td>
                <td class="px-6 py-4">{{ user.genderInterest }}</td>
              </tr>
              <tr>
                <td class="px-6 py-4 font-medium text-gray-900">School:</td>
                <td class="px-6 py-4">{{ user.school || 'N/A' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    
    <!-- Action Buttons Section -->
    <div v-if="user" class="mt-4 flex justify-between">
      <button @click="goBack" class="button-link">Back to Home</button>
      <button @click="navigateToUserEdit(user.id)" class="button-link">Edit</button>
    </div>
  
    <!-- Loading State -->
    <div v-else class="max-w-md mx-auto mt-8">
      Loading user...
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
  
    
    export default {
      name: 'Profile',
      components: {
        Galleria
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
        galleriaImages() {
        const images = this.user.images || [];
        // Fill the array with default images if necessary
        const filledImages = [...images];
        while (filledImages.length < this.numberOfImages) {
          filledImages.push(this.defaultImage);
        }
        return filledImages.map(url => ({ itemImageSrc: url, thumbnailImageSrc: url }));
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
        goBack() {
          this.$router.push({ name: 'Home' });
        },
        navigateToUserEdit(userId) {
        this.$router.push({ name: 'ProfileEdit', params: { id: userId } });
      }
      }
    };
    </script>
    
    <style scoped>
    .galleria-item {
      width: 550px;
      height: 350px;
      object-fit: cover;
      display: block;
    }
    
    .galleria-thumbnail {
      width: 50px;
      height: 50px;
      object-fit: cover;
      display: block;
    }
    
    .user-name {
      font-size: 40px;
      overflow-wrap: break-word; /* Ensure text wraps within the container */
      word-break: break-word; /* Break long words */
    }
    
    .details-title {
      font-size: 30px;
    }
    
    .table td {
      overflow-wrap: break-word; /* Ensure text wraps within table cells */
      word-break: break-word; /* Break long words */
    }
    
    .info {
      overflow-wrap: break-word; /* Ensure text wraps within this section */
      word-break: break-word; /* Break long words */
    }
    
    .button-link {
      text-decoration: none;
      color: #4b5563; /* Default text color */
      background-color: white;
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
    
    