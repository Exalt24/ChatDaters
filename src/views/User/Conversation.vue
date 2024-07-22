<template>
  <div class="flex flex-col h-full">
    <div v-if="loading" class="max-w-6xl mx-auto mt-8 mb-8 text-center">
      <p>Loading...</p>
    </div>
    <div v-else class="flex-1 overflow-hidden flex flex-col">
      <div class="conversation-header" v-if="receiver">
    <button class="button-link" @click="goBack(currentUser.id)">
      <i class="pi pi-arrow-left" style="font-size: 1.2em;"></i>
    </button>
    <button @click="openProfile(receiver)" class="profile-button">
      <div class="profile-info">
        <img :src="receiver.images[0]" alt="Receiver Photo" class="receiver-photo" />
        <h2>{{ receiver.firstName }} {{ receiver.lastName }}</h2>
      </div>
    </button>
  </div>
            
      <div class="messages-list flex-1 overflow-auto">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="{
            'message-sent': message.sender.id === currentUser.id,
            'message-received': message.sender.id !== currentUser.id,
          }"
        >
          <div :class="{
            'message-bubble-sent': message.sender.id === currentUser.id,
            'message-bubble-received': message.sender.id !== currentUser.id,
          }">
            <div class="message-content">{{ message.content }}</div>
          </div>
          <div :class="{
            'message-meta-sent': message.sender.id === currentUser.id,
            'message-meta-received': message.sender.id !== currentUser.id,
          }">{{ formatDate(message.createdAt) }}</div>
        </div>
      </div>
      <div class="message-input">
        <input v-model="newMessage" placeholder="Type a message" @keyup.enter="sendMessage" />
        <button class="button-link" @click="sendMessage"><i class="pi pi-send" style="font-size: 1.2em;"></i></button>
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
                  <td class="px-6 py-4 whitespace-nowrap">{{ formatBirthDate(selectedUser.birthdate) }}</td>
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
  import Dialog from 'primevue/dialog';
import Galleria from 'primevue/galleria';
  
  export default {
    name: 'Conversation',
    components:{
    Dialog,
    Galleria
  },
    data() {
      return {
        currentUser: null,
        newMessage: '',
        messages: [],
        receiver: null,
        loading: true,
        mostRecentMessage: null,
        updatedAt: null,
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
      galleriaImages(userImages = []) {
    console.log('galleriaImages called with:', userImages);
    const images = userImages;
    const filledImages = [...images];
    while (filledImages.length < this.numberOfImages) {
      filledImages.push(this.defaultImage);
    }
    return filledImages.map(url => ({ itemImageSrc: url, thumbnailImageSrc: url }));
  },
    formatBirthDate(dateString) {
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
    formatDate(date) {
    const today = new Date();
    const messageDate = new Date(date);

    // Helper function to format date
    const formatDateOptions = {
      weekday: 'long', // For day of the week (e.g., Monday)
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    };

    // Calculate time difference
    const timeDiff = today - messageDate;
    const daysDiff = Math.floor(timeDiff / (1000 * 60 * 60 * 24));

    if (daysDiff === 0) {
      // Today
      return `Today at ${messageDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    } else if (daysDiff === 1) {
      // Yesterday
      return `Yesterday at ${messageDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    } else if (daysDiff < 7) {
      // This week (e.g., Monday)
      return messageDate.toLocaleDateString('en-US', { weekday: 'long', hour: '2-digit', minute: '2-digit' });
    } else {
      // Older dates
      return messageDate.toLocaleDateString('en-US', formatDateOptions) + ' ' + messageDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
  },
      async fetchConversation() {
  try {
    const { conversationId } = this.$route.params;

    const { data } = await this.$apollo.query({
      query: gql`
        query GetConversation($conversationId: ID!) {
          conversation(id: $conversationId) {
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
            messages {
              id
              content
              createdAt
              sender {
                id
                firstName
                lastName
                images
              }
              receiver {
                id
                firstName
                lastName
                images
              }
            }
            mostRecentMessage {
              id
              content
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
            updatedAt
          }
        }
      `,
      variables: {
        conversationId: conversationId,
      },
    });

    this.messages = data.conversation.messages;
    this.receiver = data.conversation.users.find(user => user.id !== this.currentUser.id);
    this.mostRecentMessage = data.conversation.mostRecentMessage; // Add this line if you need to track most recent message separately
    this.updatedAt = data.conversation.updatedAt;

    this.$nextTick(() => {
      this.scrollToBottom();
    });
  } catch (error) {
    console.error('Error fetching conversation:', error);
  } finally {
    this.loading = false; // Set loading to false after fetching data
  }
},
      async sendMessage() {
  // Trim the new message and check if it's empty or only whitespace
  const trimmedMessage = this.newMessage.trim();

  if (!trimmedMessage) {
    // Display a prompt or alert if the message is empty or only whitespace
    alert('Message cannot be empty or consist only of whitespace.');
    return;
  }
  
  try {
    const { data } = await this.$apollo.mutate({
      mutation: gql`
        mutation StartConversationMutation($receiverId: ID!, $content: String!) {
          startConversationMutation(input: { receiverId: $receiverId, content: $content }) {
            message {
              id
              content
              createdAt
              sender {
                id
                firstName
                lastName
                images
              }
              receiver {
                id
                firstName
                lastName
                images
              }
            }
            errors
          }
        }
      `,
      variables: {
        receiverId: this.receiver.id,
        content: this.newMessage,
      },
      update: (cache, { data: { startConversationMutation } }) => {
  const { message, errors } = startConversationMutation;

  if (errors.length > 0) {
    console.error('Errors:', errors);
    return;
  }

  const query = gql`
    query GetConversation($conversationId: ID!) {
      conversation(id: $conversationId) {
        id
        messages {
          id
          content
          createdAt
          sender {
            id
            firstName
            lastName
            images
          }
          receiver {
            id
            firstName
            lastName
            images
          }
        }
        mostRecentMessage {
          id
          content
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
        updatedAt
      }
    }
  `;

  const existingData = cache.readQuery({
    query,
    variables: { conversationId: this.$route.params.conversationId }
  });

  if (existingData) {
    const updatedMessages = [...existingData.conversation.messages, message];

    cache.writeQuery({
      query,
      variables: { conversationId: this.$route.params.conversationId },
      data: {
        conversation: {
          ...existingData.conversation,
          messages: updatedMessages,
          mostRecentMessage: message,
          updatedAt: new Date().toISOString() // Update the `updatedAt` field
        }
      }
    });
  } else {
    console.warn('No existing data found in cache');
  }
}
    });

    console.log('Mutation response:', data);  // Log the response

    const message = data.startConversationMutation.message;

    // Create a new messages array with the existing messages and the new message
    const updatedMessages = [...this.messages, message];

    // Update local state with the new messages array
    this.messages = updatedMessages;
    this.newMessage = '';
    this.$nextTick(() => {
      this.scrollToBottom();
    });
  } catch (error) {
    console.error('Error sending message:', error.message);
  }
},
      scrollToBottom() {
        const messagesList = this.$refs.messagesList;
        if (messagesList) {
          messagesList.scrollTop = messagesList.scrollHeight;
        }
      },
      isAdminPage() {
        return this.$route.path.startsWith('/admin');
      },
      async fetchCurrentUser() {
        try {
          if (this.$apollo) {
            const response = await this.$apollo.query({
              query: gql`
                query GetCurrentUserData {
                  currentUser {
                    id
                    email
                    createdAt
                    admin
                    firstName
                    lastName
                  }
                }
              `,
            });
            this.currentUser = response.data.currentUser;
            console.log(this.currentUser)
          } else {
            console.log('Apollo is Busy');
          }
        } catch (error) {
          console.error('Fetch current user error:', error.message);
        } finally {
          this.loading = false; // Set loading to false after fetching data
        }
      },
      goBack(userId) {
        this.$router.push({ name: 'ConversationList', params: { id: userId } });
      }
    },
    async created() {
      if (localStorage.getItem('token') && !this.isAdminPage()) {
        await this.fetchCurrentUser();
        await this.fetchConversation();
      }
  
      this.$watch('$route', async () => {
        if (!this.isAdminPage() && localStorage.getItem('token')) {
          await this.fetchCurrentUser();
          await this.fetchConversation();
        } else {
          this.currentUser = null;
        }
      });
    },
  };
  </script>
  
  <style scoped>
  .conversation-header {
    display: flex;
    align-items: center;
    padding: 16px;
    background-color: #f5f5f5;
    border-bottom: 1px solid #ddd;
  }
  
  .receiver-photo {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 12px;
  }
  
  .messages-list {
    display: flex;
    flex-direction: column;
    flex: 1;
    padding: 16px;
    overflow-y: auto;
    background: #e5ddd5;
  }
  
  .message-sent {
  align-self: flex-end;
  text-align: right,
}

.message-received {
  align-self: flex-start;
  text-align: left;
}

.message-bubble-sent {
  display: flex;
  flex-direction: column;
  background-color: #dcf8c6;
  padding: 8px 12px;
  max-width: 100%; /* Adjust this value to control the max width */
  border-radius: 12px 12px 12px 0;
  margin-left: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  word-wrap: break-word; /* Ensures long words break and wrap */
}

.message-bubble-received {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 8px 12px;
  max-width: 75%; /* Adjust this value to control the max width */
  border-radius: 12px 12px 0 12px;
  margin-right: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  word-wrap: break-word; /* Ensures long words break and wrap */
}
  
  .message-content {
    margin-bottom: 4px;
    text-align: left
  }
  
  .message-meta-sent {
    margin-top: 4px; /* Add some space between the content and the timestamp */
    font-size: 0.8em;
    color: #666;
    text-align: right; /* Align the timestamp to the start of the message bubble */
  }

  .message-meta-received {
    margin-top: 4px; /* Add some space between the content and the timestamp */
    font-size: 0.8em;
    color: #666;
    text-align: left; /* Align the timestamp to the start of the message bubble */
  }
  
  .message-input {
    display: flex;
    padding: 16px;
    border-top: 1px solid #ddd;
    background: #f5f5f5;
  }
  
  .message-input input {
    flex: 1;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 20px;
    margin-right: 8px;
  }
  
  .message-input button {
    border: none;
    color: white;
    cursor: pointer;
  }
  
  .message-input button:hover {
    color: gray !important;
  }
  
  .button-link {
    text-decoration: none;
    color: #4b5563 !important;
    margin-left: 1rem;
    transition: background-color 0.3s ease;
    margin-right: 2rem;
  }
  
  .button-link:hover {
    color: gray !important;
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

.profile-button {
  display: flex;
  align-items: center;
  border: none;
  background: transparent;
  cursor: pointer;
}

.profile-button :hover{
  background-color: rgb(223, 223, 223);
  padding: 0.5rem;
  border-radius: 1rem;
}

.profile-info {
  display: flex;
  align-items: center;
}

  </style>