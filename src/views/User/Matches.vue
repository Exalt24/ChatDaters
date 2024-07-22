<template>
  <div class="matches-page">
    <div class="max-w-6xl mx-auto mt-8 mb-8 text-center" v-if="loading">Loading...</div>
    <div v-else>
      <div class="max-w-6xl mx-auto mt-8 mb-8 text-center" v-if="matches.length === 0">No matches found.</div>
      <div v-else>
        <div v-for="match in paginatedMatches" :key="match.id" class="match-card" @click="openProfile(match)">
          <img :src="match.images[0]" alt="Primary Photo" class="match-photo" />
          <div class="match-info">
            <h3>{{ match.firstName }} {{ match.lastName }}</h3>
            <p>{{ match.locationCity }}, {{ match.locationRegion }}, {{ match.locationCountry }}</p>
            <p class="updated-at">{{ timeAgo(match.updatedAt) }}</p>
          </div>
          <div class="actions">
            <button @click="startConversation(match.id, $event)" class="message-btn">
              <i class="pi pi-comment" style="font-size: 1em;"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
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
          <Dialog v-model:visible="profileDialogVisible" header="User Profile" modal>
      <div v-if="selectedUser">
        <Galleria
              :value="galleriaImages(selectedUser?.images || [])"
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
        <div class="info" style="text-align: center;">
          <div class="user-info" style="justify-content: center;">
            <strong :style="{ fontSize: '24px' }">
              <i :class="genderIcon(selectedUser.gender) + ' gender-icon'"></i>
              {{ selectedUser.firstName }} {{ selectedUser.lastName }}
              <span :style="{ marginLeft: '0.05em', fontSize: '14px', color: '#555' }">({{ calculateAge(selectedUser.birthdate) }})</span>
            </strong>
          </div>
          <p>{{ selectedUser.bio }}</p>
          <p style="display: flex; align-items: center; font-size: small; margin-top: 1rem; font-weight: bold;">
            <i class="pi pi-map-marker" style="font-size: 1.2em; margin-right: 0.5em;"></i>
            {{ selectedUser.locationCity }}, {{ selectedUser.locationRegion }}, {{ selectedUser.locationCountry }}
          </p>
        </div>
      </div>
      <div class="rounded-lg p-3 bg-gray-200">
          <strong class="block" :style="{ fontSize: '20px' }">Additional Details:</strong>
          <div class="my-5">
            <table class="min-w-full bg-white divide-y divide-gray-300">
              <tbody class="bg-white divide-y divide-gray-200">
                <tr>
                  <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Birthdate:</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ formatDate(selectedUser.birthdate) }}</td>
                </tr>
                <tr>
                  <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Sexual Orientation:</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ selectedUser.sexualOrientation }}</td>
                </tr>
                <tr>
                  <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">Gender Interest:</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ selectedUser.genderInterest }}</td>
                </tr>
                <tr>
                  <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">School:</td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ selectedUser.school || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
    </Dialog>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import Paginator from 'primevue/paginator';
import Dialog from 'primevue/dialog';
import Galleria from 'primevue/galleria';


export default {
  name: "ShowMatches",
  components:{
    Paginator,
    Dialog,
    Galleria
  },
  data() {
    return {
      loading: false,
      currentUser: null,
      matches: [],
      first: 0,
      perPage: 5,
      profileDialogVisible: false,
      selectedUser: null,
      defaultImage: '/default-user.png', // Path to your default image
      numberOfImages: 5,
    };
  },
  computed:{
    paginatedMatches() {
        const startIndex = this.first;
        const endIndex = startIndex + this.perPage;
        return this.matches.slice(startIndex, endIndex);
      },
      totalMatches() {
        return this.matches.length;
      },
  },
  methods: {
    galleriaImages(userImages = []) {
    console.log('galleriaImages called with:', userImages);
    const images = userImages;
    const filledImages = [...images];
    while (filledImages.length < this.numberOfImages) {
      filledImages.push(this.defaultImage);
    }
    return filledImages.map(url => ({ itemImageSrc: url, thumbnailImageSrc: url }));
  },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', { dateStyle: 'long' }).format(date);
    },
     openProfile(user) {
      this.selectedUser = user;
      this.profileDialogVisible = true;
    },
    closeProfile() {
      this.profileDialogVisible = false;
    },
    timeAgo(updatedAt) {
  console.log("Date:", updatedAt);
  const now = new Date();
  const updatedDate = new Date(updatedAt);
  const diffMs = now - updatedDate; // Difference in milliseconds

  const diffSecs = Math.floor(diffMs / 1000); // Convert to seconds
  const diffMins = Math.floor(diffSecs / 60); // Convert to minutes
  const diffHours = Math.floor(diffMins / 60); // Convert to hours

  if (diffSecs < 60) return `${diffSecs} sec${diffSecs > 1 ? 's' : ''} ago`;
  if (diffMins < 60) return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
  
  // For differences of 24 hours or more, you can use a different format or extend further.
  const diffDays = Math.floor(diffHours / 24);
  return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
},
    async fetchMatches() {
      this.loading = true;
      try {
        const { data } = await this.$apollo.query({
          query: gql`
            query GetMatches {
              currentUser {
                id
                matches {
                  id
                  users {
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
                    admin
                  }
                  status
                  updatedAt
                }
              }
            }
          `,
        });

        this.currentUser = data.currentUser;
        const currentUser = data.currentUser;

        const allMatches = currentUser.matches.map(match => {
          // Find the matched user who is not the current user
          const matchedUser = match.users.find(user => user.id !== currentUser.id);
          return {
            ...matchedUser,
            status: match.status,
            updatedAt: match.updatedAt
          };
        });

        this.matches = allMatches.filter(match => match.status === "matched");

        this.matches.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
      } catch (error) {
        console.error("Error fetching matches:", error);
      } finally {
        this.loading = false;
      }
    },
    async startConversation(receiverId, event) {
      event.stopPropagation(); 
      try {
        const existingConversationId = await this.checkExistingConversation(receiverId);
        if (existingConversationId) {
          console.log("Old Message")
          this.$router.push({ name: 'Conversation', params: { id: this.currentUser.id, conversationId: existingConversationId } });
        } else {
          console.log("New Message")
          const conversationId = await this.createFirstMessage(receiverId);
          this.$router.push({ name: 'Conversation', params: { id: this.currentUser.id, conversationId } });
        }
      } catch (error) {
        console.error('Error starting conversation:', error.message);
      }
    },
    async checkExistingConversation(receiverId) {
  try {

    const { data } = await this.$apollo.query({
      query: gql`
        query GetConversations {
          currentUser {
            id
            conversations {
              id
              users {
                id
              }
            }
          }
        }
      `
    });

    const currentUserConversations = data.currentUser.conversations || [];


    const existingConversation = currentUserConversations.find(convo =>
      convo.users.some(user => user.id === receiverId)
    );


    console.log("EXISTING CONVO: ", existingConversation);

    return existingConversation ? existingConversation.id : null;
  } catch (error) {
    console.error('Error checking existing conversation:', error);
    return null; // Return null in case of an error
  }
},

async createFirstMessage(receiverId) {
  try {
    const { data } = await this.$apollo.mutate({
      mutation: gql`
        mutation StartConversationMutation($receiverId: ID!, $content: String!) {
          startConversationMutation(input: { receiverId: $receiverId, content: $content }) {
            conversation {
              id
              messages {
                id
                content
                status
                createdAt
                sender {
                  id
                  firstName
                  lastName
                }
                receiver {
                  id
                  firstName
                  lastName
                }
              }
            }
            errors
          }
        }
      `,
      variables: {
        receiverId: receiverId,
        content: "Hello"
      },
      update: (cache, { data: { startConversationMutation } }) => {
        const { conversation } = startConversationMutation;
        if (conversation) {
          const conversationsQuery = gql`
            query GetConversations {
              currentUser {
                id
                conversations {
                  id
                  messages {
                    id
                    content
                    status
                    createdAt
                    sender {
                      id
                      firstName
                      lastName
                    }
                    receiver {
                      id
                      firstName
                      lastName
                    }
                  }
                }
              }
            }
          `;

          // Log the current cache data
          const existingData = cache.readQuery({ query: conversationsQuery });
          console.log('Existing data in cache:', existingData);

          if (existingData) {
            const updatedConversations = [
              ...existingData.currentUser.conversations,
              conversation
            ];

            cache.writeQuery({
              query: conversationsQuery,
              data: {
                currentUser: {
                  ...existingData.currentUser,
                  conversations: updatedConversations
                }
              }
            });
          } else {
            console.warn('No existing data found in cache');
            // Optionally write initial data if necessary
            cache.writeQuery({
              query: conversationsQuery,
              data: {
                currentUser: {
                  id: data.currentUser.id,
                  conversations: [conversation]
                }
              }
            });
          }
        }
      }
    });

    return data.startConversationMutation.conversation.id;
  } catch (error) {
    console.error('Error starting conversation:', error.message);
    throw error; // Re-throw the error to handle it in the caller method
  }
},
handlePageChange(event) {
          this.first = event.page * this.perPage;
        },
        isAdminPage() {
      return this.$route.path.startsWith('/admin');
    }, genderIcon(gender) {
      return gender === 'Male' ? 'pi pi-mars' : 'pi pi-venus';
    },
    calculateAge(birthdate) {
    const today = new Date();
    const birthDate = new Date(birthdate);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDifference = today.getMonth() - birthDate.getMonth();
    
    // If the current month is before the birth month or if it's the birth month but the current day is before the birth day
    if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    
    return age;
  },

  },
  async mounted() {
    if (localStorage.getItem('token')) {
      await this.fetchMatches();
    }

    this.$watch('$route', async () => {
      if (!this.isAdminPage() && localStorage.getItem('token')) {
        await this.fetchMatches();
      } else {
        this.matches = [];
      }
    });
  },
};
</script>

<style scoped>
.matches-page {
  padding: 20px;
}

.match-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s; /* Smooth transition for hover effect */
  cursor: pointer;
}

.match-card:hover {
  background-color: #637575;
}


.match-photo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.match-info {
  display: flex;
  flex-direction: column;
}

.match-info h3 {
  margin: 0;
  font-size: 1.2em;
}

.match-info p {
  margin: 5px 0;
  font-size: 0.9em;
}

.updated-at {
  font-size: 0.8em;
  color: #888;
}

.actions {
  text-align: right;
}

.message-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: grey;
  font-size: 2em;
}

.message-btn :hover {
  color: #A4C2C9;
}

.message-btn i {
  margin-right: 8px;
}

.info {
  text-align: center;
  padding: 16px;
  font-family: Arial, sans-serif; /* Changed font for better readability */
}

.user-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px; /* Space between name and icon */
}

.pi {
  font-size: 24px; /* Adjust size as needed */
}

.gender-icon {
  font-size: 18px; /* Adjust size as needed */
}

.gender-icon.pi-mars {
  color: #007bff; /* Blue for male */
}

.gender-icon.pi-venus {
  color: #e83e8c; /* Pink for female */
}
</style>

