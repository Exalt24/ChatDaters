module.exports = {
  client: {
    service: {
      name: 'vueapp',  // Replace with your service name
      url: 'https://chatdaters.onrender.com/graphql',  // URL to your GraphQL API
    },
    includes: [
      'src/**/*.vue',
      'src/**/*.js',
    ],
  },
};
