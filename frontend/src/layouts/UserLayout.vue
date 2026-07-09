<template>
  <div class="flex flex-col min-h-screen">
    <!-- Header Component -->
    <Header class="w-full"></Header>

    <!-- Main Content Area -->
    <main class="flex-1 bg-[#d7d7d7] py-6 w-full">
      <!-- Your router-view where dynamic content will be rendered -->
      <router-view class="w-full"></router-view>
    </main>

    <!-- Footer Component -->
    <Footer class="w-full"></Footer>
  </div>
</template>

<script>
import Header from './../components/User/Header.vue'
import Footer from './../components/User/Footer.vue'

export default {
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped>
/* Ensure full width for body and html */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
</style>
