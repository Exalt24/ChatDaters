import { createApp } from 'vue';
import { createApolloProvider } from '@vue/apollo-option';
import apolloClient from './apolloclient';
import App from './App.vue'
import router from './router'
import './input.css'
import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/tailwind-light/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import InputText from 'primevue/inputtext';
import Avatar from 'primevue/avatar';
import Menu from 'primevue/menu';
import Tooltip from 'primevue/tooltip';
import Dialog from 'primevue/dialog';
import Vue3Toasity from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';




const apolloProvider = createApolloProvider({
  defaultClient: apolloClient,
});

createApp(App)
  .component('InputText', InputText)
  .component('Avatar', Avatar)
  .component('Menu', Menu)
  .component('Dialog', Dialog)
  .directive('tooltip', Tooltip)
  .use(router)
  .use(apolloProvider)
  .use(PrimeVue)
  .use(Vue3Toasity, { autoClose: 2000})
  .mount('#app')
