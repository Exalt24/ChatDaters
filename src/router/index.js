import { createRouter, createWebHistory } from 'vue-router';
import AdminLayout from '@/layouts/AdminLayout.vue';
import UserLayout from '@/layouts/UserLayout.vue';
import Home from '@/views/Home.vue';
import Login from '@/views/Login.vue';
import Signup from '@/views/Signup.vue';
import AdminDashboard from '@/views/Admin/Dashboard.vue';
import AdminMatches from '@/views/Admin/Match/AdminMatches.vue';
import ShowMatches from '@/views/Admin/Match/ShowMatches.vue';
import AdminUsers from '@/views/Admin/User/AdminUsers.vue';
import ShowUsers from '@/views/Admin/User/ShowUsers.vue';
import ShowUser from '@/views/Admin/User/ShowUser.vue';
import EditUser from '@/views/Admin/User/EditUser.vue';
import Matches from '@/views/User/Matches.vue';
import Profile from '@/views/User/Profile.vue';
import Swipe from '@/views/User/Swipe.vue';
import ProfileEdit from '@/views/User/ProfileEdit.vue';
import ConversationList from '@/views/User/ConversationList.vue';
import Conversation from '@/views/User/Conversation.vue';

const routes = [
  {
    path: '/',
    component: UserLayout, // Use UserLayout for user routes
    children: [
      { path: '', name: "Home", component: Home },
      { path: 'login', name: "Login", component: Login },
      { path: 'signup', name: "Signup", component: Signup },
      { path: ':id/profile', name: "Profile", component: Profile, meta: { requiresAuth: true } },
      { path: ':id/swipe', name: "Swipe", component: Swipe, meta: { requiresAuth: true } },
      { path: ':id/profile/edit', name: "ProfileEdit", component: ProfileEdit, meta: { requiresAuth: true } },
      { path: ':id/conversations', name: 'ConversationList', component: ConversationList, meta: { requiresAuth: true } },
      { path: ':id/conversations/:conversationId', name: 'Conversation', component: Conversation, meta: { requiresAuth: true } },
      { path: ':id/matches', name: 'ShowMatches', component: Matches, meta: { requiresAuth: true } },
    ]
  },
  {
    path: '/admin',
    component: AdminLayout, // Use AdminLayout for admin routes
    children: [
      { path: '', name: "Dashboard", component: AdminDashboard },
      { 
        path: 'matches', 
        component: AdminMatches, // Nested route under AdminMatches
        children: [
          { path: '', name: 'Matches', component: ShowMatches },
        ]
      },
      { 
        path: 'users',  
        component: AdminUsers,
        children: [
          { path: '', name: 'Users', component: ShowUsers },
          { path: ':id', name: 'Show User', component: ShowUser },
          { path: ':id/edit', name: 'Edit User', component: EditUser }
        ] 
      }
    ]
  },
  // Catch-all route for undefined user routes
  {
    path: '/:catchAll(.*)',
    redirect: to => {
      // Redirect to home for undefined user routes
      if (to.path.startsWith('/admin')) {
        return '/admin';
      } else {
        return '/';
      }
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth;
  const isLoggedIn = !!localStorage.getItem('token'); // Replace with your actual authentication check

  if (requiresAuth && !isLoggedIn) {
    sessionStorage.setItem('redirectAfterLogin', JSON.stringify({ name: to.name, params: to.params, query: to.query }));
    next('/login'); // Redirect to login page
  } else {
    next(); // Allow navigation
  }
});

export default router;
