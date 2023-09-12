<template>
  <div>
    <input ref="searchInput" type="text" placeholder="Search..." @input="onInputChange" />
    <ul v-if="searchResults.length > 0" class="dropdown">
      <li v-for="result in searchResults" :key="result.id" @click="selectTrack(result)">
        {{ result.name }}
      </li>
    </ul>
  </div>

  <div class="slider">
  <label for="limit">Limit: {{ limit }}</label>
    <input
      type="range"
      id="limit"
      min="1"
      max="100"
      v-model="limit"
    />
  </div>

  <div class="slider">
    <label for="acousticness">Acousticness: {{ acousticness }}</label>
    <input
      type="range"
      id="acousticness"
      step="0.01"
      min="0"
      max="1"
      v-model="acousticness"
    />
  </div>

  <div class="slider">
    <label for="danceability">Danceability: {{ danceability }}</label>
    <input
      type="range"
      id="danceability"
      step="0.01"
      min="0"
      max="1"
      v-model="danceability"
    />
  </div>

  <div class="slider">
    <label for="energy">Energy: {{ energy }}</label>
    <input
      type="range"
      id="energy"
      step="0.01"
      min="0"
      max="1"
      v-model="energy"
    />
  </div>

  <div class="slider">
    <label for="instrumentalness">Instrumentalness: {{ instrumentalness }}</label>
    <input
      type="range"
      id="instrumentalness"
      step="0.01"
      min="0"
      max="1"
      v-model="instrumentalness"
    />
  </div>

  <div class="slider">
    <label for="liveness">Liveness: {{ liveness }}</label>
    <input
      type="range"
      id="liveness"
      step="0.01"
      min="0"
      max="1"
      v-model="liveness"
    />
  </div>

  <div class="slider">
    <label for="loudness">Loudness: {{ loudness }}</label>
    <input
      type="range"
      id="loudness"
      step="0.01"
      min="-60"
      max="0"
      v-model="loudness"
    />
  </div>

  <div class="slider">
    <label for="popularity">Popularity: {{ popularity }}</label>
    <input
      type="range"
      id="popularity"
      min="0"
      max="100"
      v-model="popularity"
    />
  </div>

  <div class="slider">
    <label for="speechiness">Speechiness: {{ speechiness }}</label>
    <input
      type="range"
      id="speechiness"
      step="0.01"
      min="0"
      max="1"
      v-model="speechiness"
    />
  </div>

  <div class="slider">
    <label for="tempo">Tempo: {{ tempo }}</label>
    <input
      type="range"
      id="tempo"
      step="1"
      min="60"
      max="200"
      v-model="tempo"
    />
  </div>

  <div class="slider">
    <label for="valence">Valence: {{ valence }}</label>
    <input
      type="range"
      id="valence"
      step="0.01"
      min="0"
      max="1"
      v-model="valence"
    />
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
      limit: 5,
      seed_tracks: '',
      acousticness: 0.5,
      danceability: 0.5,
      energy: 0.5,
      instrumentalness: 0.5,
      liveness: 0.5,
      loudness: 0,
      popularity: 50,
      speechiness: 0.5,
      tempo: 120,
      valence: 0.5,
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