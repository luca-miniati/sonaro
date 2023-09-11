<template>
    <div class="profilepage">
      <h2>Profile</h2>
      <p>Logged in as {{ userData.display_name }}</p>
    </div>
  </template>
  
<script>
import { mapGetters } from 'vuex';

export default {
  name: 'ProfilePage',
  data() {
    return {
      userData: {}
    };
  },
  created() {
    this.getUserData();
  },
  methods: {
    ...mapGetters(['getAccessToken']),
    async getUserData() {
      const url = `https://api.spotify.com/v1/me`;
      const headers = {
        Authorization: `Bearer ${this.getAccessToken()}`
      };

      try {
        const response = await fetch(url, {
          method: "GET",
          headers: headers,
        });

        if (response.ok) {
          const userData = await response.json();
          this.userData = userData;
        } else {
          console.error("Failed to fetch user data");
        }
      } catch (error) {
        console.error("An error occurred:", error);
      }
    }
  }
};
</script>

<style scoped>
.profilepage {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 70vh; /* Make the container cover the viewport height */
  text-align: center;
}
</style>




