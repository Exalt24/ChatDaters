<template>
  <div class="flex flex-col h-full">
    <div v-if="loading" class="loading-state">
      <p>Loading...</p>
    </div>
    <div v-else class="flex-1 overflow-hidden flex flex-col">
      <div class="conversation-header" v-if="receiver">
        <button class="button-link" @click="goBack(currentUser.id)">Back</button>
        <img :src="receiver.images[0]" alt="Receiver Photo" class="receiver-photo" />
        <h2>{{ receiver.firstName }} {{ receiver.lastName }}</h2>
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
          <div class="message-bubble">
            <div class="message-content">{{ message.content }}</div>
            <div class="message-meta">
              {{ formatDate(message.createdAt) }}
            </div>
          </div>
        </div>
      </div>
      <div class="message-input">
        <input v-model="newMessage" placeholder="Type a message" @keyup.enter="sendMessage" />
        <button class="button-link" @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import gql from 'graphql-tag';
  
  export default {
    name: 'Conversation',
    data() {
      return {
        currentUser: null,
        newMessage: '',
        messages: [],
        receiver: null,
        loading: true,
        mostRecentMessage: null,
        updatedAt: null,
      };
    },
    methods: {
      formatDate(date) {
        return new Date(date).toLocaleString();
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
              images
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
  margin: 10px;
  padding: 8px 12px;
  max-width: 60%;
  border-radius: 12px 12px 0 12px;
  background-color: #dcf8c6;
}

.message-received {
  align-self: flex-start;
  margin: 10px;
  padding: 8px 12px;
  max-width: 60%;
  border-radius: 12px 12px 12px 0;
  background-color: #fff;
}

.message-bubble {
  display: flex;
  flex-direction: column;
}

.message-content {
  margin-bottom: 4px;
}

.message-meta {
  font-size: 0.8em;
  color: #666;
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
  padding: 12px 20px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 20px;
  cursor: pointer;
}

.message-input button:hover {
  background-color: #0056b3;
}
  
  .button-link {
    text-decoration: none;
    color: #4b5563 !important;
    background-color: transparent !important;
    border: 1px solid #4b5563 !important;
    padding: 8px 16px;
    border-radius: 4px;
    transition: background-color 0.3s ease;
    margin-right: 1rem;
  }
  
  .button-link:hover {
    background-color: #4b5563 !important;
    color: white !important;
  }
  </style>