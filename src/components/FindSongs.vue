<template>
  <div>
    <input ref="searchInput" type="text" placeholder="Search..." @input="onInputChange" />
    <ul v-if="searchResults.length > 0" class="dropdown">
      <li v-for="result in searchResults" :key="result.id" @click="selectTrack(result)">
        {{ result.name }}
      </li>
    </ul>
  </div>
  <div class="selected-tracks">
    <h2>Selected Tracks</h2>
    <ul>
      <li v-for="track in selectedTracks" :key="track.id">
        {{ track.name }}
      </li>
    </ul>
  </div>
  <button @click="fetchRecommendations">Get Recommendations</button>
  <div v-if="recommendedTracks.length > 0" class="recommended-tracks">
    <h2>Recommended Tracks</h2>
    <ul>
      <li v-for="track in recommendedTracks" :key="track.id">
        {{ track.name }} by {{ track.artists[0].name }}
      </li>
    </ul>
  </div>
</template>
  
<script>
import { mapGetters } from 'vuex';

export default {
  name: 'FindTracks',
  data() {
    return {
      searchResults: [],
      selectedTracks: [],
      recommendedTracks: [],
    };
  },
  methods: {
    ...mapGetters(['getAccessToken']),
    async onInputChange() {
      const query = this.$refs.searchInput.value;
      if (query.length === 0) {
        this.searchResults = [];
        return;
      }

      const url = `https://api.spotify.com/v1/search?` +
        `q=${query}` +
        `&type=track` +
        `&limit=5`;
      const headers = {
        Authorization: `Bearer ${this.getAccessToken()}`,
      };

      const response = await fetch(url, {
        method: "GET",
        headers: headers,
      });
      
      if (response.status === 200) {
        const data = await response.json();
        if (data.tracks && data.tracks.items) {
            this.searchResults = data.tracks.items;
        } else {
          this.searchResults = [];
        }
      } else {
        this.searchResults = [];
      }
    },
    selectTrack(track) {
      this.selectedTracks.push(track);
      this.searchResults = [];
      this.$refs.searchInput.value = '';
    },
    async fetchRecommendations() {
      const trackIds = this.selectedTracks.map(track => track.id).join(',');

      const url = `https://api.spotify.com/v1/recommendations?`
      + `seed_tracks=${trackIds}`
      + `&limit=10`;
      const headers = {
        Authorization: `Bearer ${this.getAccessToken()}`,
      };
      const response = await fetch(url, {
        method: "GET",
        headers: headers,
      });

      const data = await response.json();
      this.recommendedTracks = data.tracks;
    },
  }
};
</script>

<style scoped>
.dropdown {
  list-style: none;
  padding: 0;
  margin: 0;
  border: 1px solid #ccc;
  max-height: 150px;
  overflow-y: auto;
}

.dropdown li {
  padding: 5px;
  cursor: pointer;
}

.dropdown li:hover {
  background-color: #f0f0f0;
}

h2 {
  padding: 25px;
}

li {
  padding: 10px;
}
</style>