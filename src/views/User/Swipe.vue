<template>
  <div>
    <div v-if="users.length === 0" class="max-w-6xl mx-auto mt-8 mb-8 text-center">
      <p>No more users left for this session.</p>
    </div>
    <div v-else>
      <div class="swipe-container" ref="cardContainer">
        <div
          v-for="(user, index) in users"
          :key="user.id"
          class="card"
          :style="cardStyle(index)"
        >
          <img :src="user.images[0]" alt="Profile Image" />
          <div class="info">
            <div class="user-info">
              <strong class="block text-center" :style="{ fontSize: '24px' }">
                <i :class="genderIcon(user.gender) + ' gender-icon'"></i>
                {{ user.firstName }} {{ user.lastName }}
                <span :style="{ marginLeft: '0.05em', fontSize: '14px', color: '#555' }">({{ calculateAge(user.birthdate) }})</span>
              </strong>
            </div>
            <p>{{ user.bio }}</p>
            <p style="display: flex; align-items: center; font-size: small; margin-top: 1rem; font-weight: bold;">
              <i class="pi pi-map-marker" style="font-size: 1.2em; margin-right: 0.5em;"></i>
              {{ user.locationCity }}, {{ user.locationRegion }}, {{ user.locationCountry }}
            </p>
            <!-- Information Icon -->
            <button @click.stop="openProfile(user)" class="info-icon-btn">
              <i class="pi pi-info-circle"></i>
            </button>
          </div>
        </div>
      </div>
      <div class="btns">
        <img src="/nope.png" @click="dislike" />
        <img src="/like.png" @click="like" />
      </div>
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
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import Hammer from 'hammerjs';
import Dialog from 'primevue/dialog';
import Galleria from 'primevue/galleria';

export default {
  name: "Swipe",
  components: {
    Dialog,
    Galleria
  },
  data() {
    return {
      users: [],
      currentUser: null,
      loading: true,
      currentCardIndex: 0,
      cardOffsetX: 0,
      cardOffsetY: 0,
      profileDialogVisible: false,
      selectedUser: null,
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
    handleSwipe(direction) {
  if (direction === 'like') {
    this.like();
  } else if (direction === 'dislike') {
    this.dislike();
  }
  // Move to the next card, but ensure the index doesn't go out of bounds
  this.currentCardIndex = Math.min(this.currentCardIndex, this.users.length - 1);
  // Reset card offsets
  this.resetCard();
},
    resetCard() {
      this.cardOffsetX = 0;
      this.cardOffsetY = 0;
    },
    async like() {
  const matchedUserId = this.users[this.currentCardIndex]?.id; // Get the ID of the top card
  console.log(matchedUserId);

  if (!matchedUserId) {
    console.error('No user found for like action.');
    return;
  }

  console.log("Liked User:", this.users[this.currentCardIndex]);

  try {
    const { data } = await this.$apollo.mutate({
      mutation: gql`
        mutation MatchUserMutation($matchedUserId: ID!) {
          matchUserMutation(input: { matchedUserId: $matchedUserId }) {
            match {
              id
              users {
                id
                firstName
                lastName
              }
              status
            }
            errors
          }
        }
      `,
      variables: { matchedUserId },
      update: (cache, { data: { matchUserMutation } }) => {
        const { match, errors } = matchUserMutation;

        if (errors && errors.length > 0) {
          console.error(errors.join(', '));
          return;
        }

        const matchQuery = gql`
          query GetMatches {
            currentUser {
              matches {
                id
                users {
                  id
                }
                status
              }
            }
          }
        `;

        const existingData = cache.readQuery({ query: matchQuery });
        console.log('Existing data in cache:', existingData);

        if (existingData) {
          const updatedMatches = [
            ...existingData.currentUser.matches.filter(
              m => !m.users.some(u => u.id === matchedUserId)
            ),
            match
          ];

          cache.writeQuery({
            query: matchQuery,
            data: {
              currentUser: {
                ...existingData.currentUser,
                matches: updatedMatches,
              },
            },
          });
        } else {
          console.warn('No existing data found in cache');
          cache.writeQuery({
            query: matchQuery,
            data: {
              currentUser: {
                matches: [match]
              }
            }
          });
        }
      },
    });

    const matchStatusQuery = await this.$apollo.query({
      query: gql`
        query GetMatches {
          currentUser {
            matches {
              id
              users {
                id
              }
              status
            }
          }
        }
      `,
    });

    const currentUserMatches = matchStatusQuery.data.currentUser.matches;
    const matchedMatch = currentUserMatches
      .filter(m => m.status === 'matched')
      .find(m => m.users.some(u => u.id === matchedUserId));

    if (matchedMatch) {
      console.log("Match found:", matchedMatch);
      toast.success("You have matched with this user!");
    } else {
      toast.success("User liked!");
    }

    this.users.splice(this.currentCardIndex, 1);

  } catch (error) {
    console.error("Error occurred:", error.message);
  }
},

dislike() {
  toast.error("User disliked!");
  this.users.splice(this.currentCardIndex, 1);
},

cardStyle(index) {
  // The top card should have the highest z-index
  const baseZIndex = 10;
  const zIndex = baseZIndex + (this.users.length - index);

  // Apply transform styles only for the top card
  if (index === this.currentCardIndex) {
    return {
      transform: `translateX(${this.cardOffsetX}px) translateY(${this.cardOffsetY}px)`,
      transition: 'transform 0s',
      zIndex: zIndex, // Higher z-index for the top card
    };
  } else {
    // For other cards, apply a lower z-index and reset the transform
    return {
      transform: 'translateX(0) translateY(0)',
      zIndex: baseZIndex + (this.users.length - index - 1), // Lower z-index for cards behind
    };
  }
}
, async fetchUsers() {
      this.loading = true;
      try {
        const currentUser = this.currentUser;
        const allUsersResponse = await this.$apollo.query({
          query: gql`
            query GetAllUsers {
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
            }
          `,
        });

        const allUsers = allUsersResponse.data.users;
    const nonAdminAndSelfUsers = allUsers.filter(user => !user.admin && user.id !== currentUser.id);

        // Filter based on genderInterest
        const filteredUsers = nonAdminAndSelfUsers.filter(user => {
          if (currentUser.genderInterest === 'Any') {
            return true; // Show all users if interest is "Both"
          }
          return user.gender === currentUser.genderInterest;
        });

        let matchedUserIds = [];
        if (currentUser && currentUser.matches) {
          currentUser.matches.forEach(match => {
            if (match.userReceived && match.userReceived.id === currentUser.id) {
              matchedUserIds = currentUser.matches
                .filter(match => match.status === "matched")
                .flatMap(match => match.users.map(user => user.id))
                .filter(id => id !== currentUser.id);
            } else {
              matchedUserIds = currentUser.matches
                .filter(match => ["matched", "pending"].includes(match.status))
                .flatMap(match => match.users.map(user => user.id))
                .filter(id => id !== currentUser.id);
            }
          });
        }

        const nonMatchedUsers = filteredUsers.filter(user =>
          !matchedUserIds.includes(user.id)
        );

        this.users = nonMatchedUsers.sort(() => 0.5 - Math.random());
      } catch (error) {
        console.error('Error fetching users:', error.message);
      } finally {
        this.loading = false;
      }
    },
    async fetchCurrentUser() {
      try {
        const response = await this.$apollo.query({
          query: gql`
            query GetCurrentUserData {
              currentUser {
                id
                genderInterest
                matches {
                  users {
                    id
                  }
                  userReceived {
                    id
                  }
                  status
                }
              }
            }
          `,
        });
        this.currentUser = response.data.currentUser;
      } catch (error) {
        console.error('Error fetching current user:', error.message);
      }
    },
    isAdminPage() {
      return this.$route.path.startsWith('/admin');
    },
    genderIcon(gender) {
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
  openProfile(user) {
      this.selectedUser = user;
      this.profileDialogVisible = true;
    },
    closeProfile() {
      this.profileDialogVisible = false;
    },
  },
  async mounted() {
    if (localStorage.getItem('token') && !this.isAdminPage()) {
      await this.fetchCurrentUser();
      await this.fetchUsers();
    }
    if (this.users.length !== 0) {
    const element = this.$refs.cardContainer;
  const mc = new Hammer(element);
  
  mc.get('pan').set({ direction: Hammer.DIRECTION_ALL });

  mc.on('pan', (e) => {
    if (e.target.closest('.card')) { // Ensure swipe is on the card
      if (e.isFinal) {
        if (Math.abs(e.deltaX) > 100) {
          this.handleSwipe(e.deltaX > 0 ? 'like' : 'dislike');
        } else {
          this.resetCard();
        }
      } else {
        this.cardOffsetX = e.deltaX;
        this.cardOffsetY = e.deltaY;
      }
    }
  });
}


    this.$watch('$route', async () => {
      if (!this.isAdminPage() && localStorage.getItem('token')) {
        await this.fetchCurrentUser();
        await this.fetchUsers();
      } else {
        this.currentUser = null;
      }
    });
  },
};
</script>

<style scoped>
.swipe-container {
  position: relative;
  width: 100%;
  max-width: 460px; /* Adjusted max width */
  margin: auto;
  height: 500px;
}

.card {
  position: absolute;
  width: 100%;
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0s;
}

.card img {
  width: 100%;
  height: 400px; /* Fixed height for images */
  object-fit: cover; /* Ensures the image covers the container without distortion */
}

.info {
  text-align: center;
  padding: 16px;
  font-family: Arial, sans-serif; /* Changed font for better readability */
}

.info-icon-btn {
  position: absolute;
  top: 10px; /* Adjust as needed */
  right: 10px; /* Adjust as needed */
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5em;
  color: #fff; /* Adjust color as needed */
}

.info-icon-btn:hover {
  color: gray; /* Darker color on hover */
}

.btns {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px; /* Increased space between buttons */
  margin-top: 70px;
}

.btns img {
  width: 60px; /* Increased button size for better visibility */
  height: 60px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Enhanced shadow for better depth */
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s; /* Smooth transition for button hover effect */
}

.btns img:hover {
  transform: scale(1.1); /* Slightly enlarge button on hover */
}

.card-enter-active, .card-leave-active {
  transition: opacity 0.3s;
}

.card-enter, .card-leave-to {
  opacity: 0;
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
