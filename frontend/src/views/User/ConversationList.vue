<template>
  <div class="conversations-page">
    <div class="max-w-6xl mx-auto mt-8 mb-8 text-center" v-if="loading">Loading...</div>
    <div v-else>
      <div class="max-w-6xl mx-auto mt-8 mb-8 text-center" v-if="conversations.length === 0">No conversations found.</div>
      <div v-else>
        <div v-for="conversation in paginatedConversations" :key="conversation.conversationId" class="conversations-card" @click="viewConversation(currentUser.id, conversation.conversationId)">
      <img :src="conversation.images[0]" alt="Primary Photo" class="conversations-photo" />
      <div class="conversations-info">
        <h3>{{ conversation.firstName }} {{ conversation.lastName }}</h3>
        <p class="most-recent-message">
          <strong>{{ conversation.mostRecentMessageSender }}:</strong> {{ conversation.mostRecentMessageContent }}
        </p>
      </div>
      <p class="updated-at">{{ timeAgo(conversation.updatedAt) }}</p>
    </div>
    </div>
    </div>
    <div class="flex justify-center items-center mt-4">
      <Paginator
        v-model:first="first"
        :totalRecords="totalConversations"
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
</template>

<script>
import gql from 'graphql-tag';
import Paginator from 'primevue/paginator';

export default {
  name: "ShowConversations",
  components: {
    Paginator
  },
  data() {
    return {
      loading: false,
      currentUser: null,
      conversations: [],
      first: 0,
      perPage: 5,
    };
  },
  computed: {
    paginatedConversations() {
      const startIndex = this.first;
      const endIndex = startIndex + this.perPage;
      return this.conversations.slice(startIndex, endIndex);
    },
    totalConversations() {
      return this.conversations.length;
    },
  },
  methods: {
    timeAgo(updatedAt) {
      const now = new Date();
      const updatedDate = new Date(updatedAt);
      const diffMs = now - updatedDate; // Difference in milliseconds

      const diffSecs = Math.floor(diffMs / 1000); // Convert to seconds
      const diffMins = Math.floor(diffSecs / 60); // Convert to minutes
      const diffHours = Math.floor(diffMins / 60); // Convert to hours

      if (diffSecs < 60) return `${diffSecs} sec${diffSecs > 1 ? 's' : ''} ago`;
      if (diffMins < 60) return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`;
      if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;

      const diffDays = Math.floor(diffHours / 24);
      return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    },
    async fetchConversations() {
      this.loading = true;
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
                    firstName
                    lastName
                    images
                    bio
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
                  updatedAt
                  mostRecentMessage {
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
                }
              }
            }
          `,
        });

        this.currentUser = data.currentUser;
        const currentUser = data.currentUser;

        const allConversations = currentUser.conversations.map(conversation => {
          const conversationUser = conversation.users.find(user => user.id !== currentUser.id);
          const isCurrentUserSender = conversation.mostRecentMessage.sender.id === currentUser.id;
          return {
            ...conversationUser,
            updatedAt: conversation.updatedAt,
            conversationId: conversation.id,
            mostRecentMessageContent: conversation.mostRecentMessage.content,
            mostRecentMessageSender: isCurrentUserSender ? 'You' : `${conversationUser.firstName}`
          };
        });

        this.conversations = allConversations;

        this.conversations.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
      } catch (error) {
        console.error("Error fetching conversations:", error.message);
      } finally {
        this.loading = false;
      }
    },
    viewConversation(id, conversationId) {
      this.$router.push({ name: 'Conversation', params: { id, conversationId } });
    },
    handlePageChange(event) {
      this.first = event.page * this.perPage;
    },
  },
  async mounted() {
    if (localStorage.getItem('token')) {
      await this.fetchConversations();
    }

    this.$watch('$route', async (to, from) => {
  if (!this.isAdminPage() && localStorage.getItem('token')) {
    await this.fetchConversations();
  } else {
    this.conversations = [];
  }
});
  },
};
</script>

<style scoped>
.conversations-page {
  padding: 20px;
}

.conversations-card {
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
  cursor: pointer;
  transition: background-color 0.3s; /* Smooth transition for hover effect */
}

.conversations-card:hover {
  background-color: #bdc1c1;
}

.conversations-photo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.conversations-info {
  display: flex;
  flex-direction: column;
}

.conversations-info h3 {
  margin: 0;
  font-size: 1.2em;
}

.conversations-info p {
  margin: 5px 0;
  font-size: 0.9em;
}

.updated-at {
  font-size: 0.8em;
  color: #888;
  justify-self: end;
  bottom: 0;
}

.most-recent-message {
  margin-top: 10px;
  font-size: 0.9em;
  color: #333;
}
</style>

