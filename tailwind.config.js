/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        'light-brown': '#988782', // Replace with your desired color code
      },
    },
  },
  plugins: [],
}

