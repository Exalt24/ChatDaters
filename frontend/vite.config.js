import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import path from 'path';

export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'vue': 'vue/dist/vue.esm-bundler.js',
      // Adjust the alias to point directly to the createUploadLink.mjs file
      'apollo-upload-client': path.resolve(__dirname, 'node_modules/apollo-upload-client/createUploadLink.mjs')
    }
  },
  optimizeDeps: {
    include: ['apollo-upload-client']
  }
});
