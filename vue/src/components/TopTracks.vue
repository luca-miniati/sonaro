<template>
    <div class="toptracks">
        <li v-for="track in trackData.items" :key="track.id">{{ track.name }}</li>
    </div>
  </template>
  
<script>
import { mapGetters } from 'vuex';

export default {
  name: 'TopTracks',
  data() {
    return {
      trackData: {}
    };
  },
  created() {
    this.getTrackData();
  },
  methods: {
    ...mapGetters(['getAccessToken']),
    async getTrackData() {
      const url = `https://api.spotify.com/v1/me/top/tracks`;
      const headers = {
        Authorization: `Bearer ${this.getAccessToken()}`
      };

      try {
        const response = await fetch(url, {
          method: "GET",
          headers: headers,
        });

        if (response.ok) {
          const trackData = await response.json();
          this.trackData = trackData; // Update the userData state with fetched data
          console.log(trackData); // You can log the data if needed
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




