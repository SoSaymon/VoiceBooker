import React from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import ReactDOM from 'react-dom/client';
import App from './App';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { ApolloProvider, ApolloClient, InMemoryCache } from '@apollo/client';
import { AuthProvider } from 'react-auth-kit'

const root = ReactDOM.createRoot(document.getElementById('root'));

export const client = new ApolloClient({
  uri: 'http://localhost:8000/',
  cache: new InMemoryCache()
});



root.render(
  <React.StrictMode>
    <ToastContainer
      position="top-right"
      autoClose={5000}
      hideProgressBar={false}
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      pauseOnHover
      theme="dark"
    // transition: Bounce,
    />
    {/* Same as */}
    <ToastContainer />

    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>

</React.StrictMode>
);





