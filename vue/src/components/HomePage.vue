<template>
  <div class="homepage">
    <h2>Welcome to Spotify Playground!</h2>
    <p>Discover personalized music recommendations based on your preferences.</p>
    <a @click=getUserAuthorization class="login-button">Log In with Spotify</a>
  </div>
</template>

<script>
import { v4 } from 'uuid';

// const title = document.getElementById('title');
// title.innerHTML = 'Spotify Playground';

export default {
  name: 'HomePage',
  methods: {
    getUserAuthorization() {
      const client_id = process.env.VUE_APP_CLIENT_ID;
      const redirect_uri = encodeURIComponent('http://localhost:8000/callback');
      const state = v4();
      const scope = 'user-read-private user-read-recently-played playlist-read-private playlist-read-collaborative user-top-read';

      const authorizationUrl = `https://accounts.spotify.com/authorize?` +
        `response_type=code` +
        `&client_id=${client_id}` +
        `&redirect_uri=${redirect_uri}` +
        `&state=${state}` +
        `&scope=${scope}`;

      window.location.href = authorizationUrl;
    }
  }
};
</script>

<style scoped>
.homepage {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 70vh; /* Make the container cover the viewport height */
  text-align: center;
}

.login-button {
  background-color: #e246ab;
  color: white;
  text-decoration: none;
  padding: 15px 30px; /* Add padding horizontally */
  border-radius: 30px;
  font-weight: bold;
  transition: background-color 0.2s ease-in-out; /* Add a smooth transition */
}

.login-button:hover {
  background-color: #c42c91; /* Change background color on hover */
}

h2, p, .login-button {
  margin-bottom: 30px;
}
</style>




