import { ApolloClient, InMemoryCache } from '@apollo/client/core';
import createUploadLink from 'apollo-upload-client';
import { setContext } from '@apollo/client/link/context';

const getCsrfToken = () => {
  const csrfMetaTag = document.querySelector('meta[name="csrf-token"]');
  return csrfMetaTag ? csrfMetaTag.getAttribute('content') : '';
};

const uploadLink = createUploadLink({
  uri: 'https://chatdaters.onrender.com/graphql'
  // uri: 'http://localhost:3000/graphql'
});

const authLink = setContext((_, { headers }) => {
  // Get CSRF token
  const csrfToken = getCsrfToken();
  
  // Get JWT token from localStorage
  const authToken = localStorage.getItem('token');

  // Check if authToken is defined and not empty before including in headers
  if (authToken) {
    console.log("JWT TOKEN:", authToken)
    headers = {
      ...headers,
      Authorization: `Bearer ${authToken}`,
    };
  }

  return {
    headers: {
      ...headers,
      'X-CSRF-Token': csrfToken,
    }
  };
});

const apolloClient = new ApolloClient({
  link: authLink.concat(uploadLink),
  cache: new InMemoryCache(),
  connectToDevTools: true,
});



export default apolloClient;
