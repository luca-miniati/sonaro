<template>
  <div class="get-recommendations">
    <div class="outer-section">
      <div class="inner-section">
        <p>Seed Tracks</p>
        <button class="add-songs-button" @click="onClick">
          <img src="@/assets/addsongs.png">
          <p>Add Songs</p>
        </button>
        <ul v-if="searchResults.length > 0" class="dropdown">
          <li v-for="result in searchResults" :key="result.id" @click="selectTrack(result)">
            <img :src="result.album.images[0].url">
            <p class="song-name">{{ result.name }}</p>
            <p v-for="artist in result.artists" :key="artist.id" class="artist-name">{{ artist.name }}</p>
          </li>
        </ul>
      </div>
    </div>
    <div class="outer-section">
      <p>Settings</p>

    </div>

    <div class="get-recommendations-button">
      <img src="@/assets/getrecommendations.png">
      <a @click=getRecommendations>Get Recommendations</a>
    </div>
  </div>

  <div class="sliders">

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
import { mapGetters } from "vuex";
import axios from 'axios';

export default {
  name: "FindTracks",
  data() {
    return {
      searching: false,
      searchResults: [],
      selectedTracks: [],
      recommendedTracks: [],
      limit: 5,
      seed_tracks: "",
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
    ...mapGetters(["getAccessToken"]),
    onClick () {
      if (!this.searching) {
        let searchInput = this.searchInput();
        const button = document.querySelector(".add-songs-button");

        button.querySelector("img").style.display = "none";
        button.querySelector("p").style.display = "none";
        button.appendChild(searchInput);
        searchInput.focus();
        this.searching = true;
      }
    },
    async onInputChange(query) {
      if (query.length === 0) {
        this.searchResults = [];
        return;
      }

      const currentTime = new Date().getTime();
      if(currentTime >= this.$store.getters.tokenExpiration) {
        const refreshOptions = {
        url: '/refresh_token',
        params: {
          refresh_token: this.$store.getters.refreshToken
        }
      }

      axios.get(refreshOptions.url, {params: refreshOptions.params})
        .then(response => {
          this.$store.commit('SET_ACCESS_TOKEN', response.data.access_token); 

          const expiration = new Date().getTime() + response.data.expires_in * 1000;
          this.$store.commit('SET_TOKEN_EXPIRATION', expiration);
        })
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
    searchInput() {
      let elem = document.createElement("input");
      elem.ref = "searchInput";
      elem.type = "text";
      elem.placeholder = "Search...";
      elem.style.height = "5vh";
      elem.style.border = "none";
      elem.style.outline = "none";
      elem.style.backgroundColor = "#0D0D0D";
      elem.style.borderRadius = "5px";
      elem.style.color = "#ffffff";
      elem.style.textIndent = "10px";
      elem.classList.add("search-input");

      elem.addEventListener("input", (event) => {
        this.onInputChange(event.target.value);
      });

      return elem;
    },
    selectTrack(track) {
      console.log(track)
      this.selectedTracks.push(track);
      this.searchResults = [];

      const searchInput = document.querySelector(".search-input")
      searchInput.value = "";

      this.searching = false;

      const button = document.querySelector(".add-songs-button");
      button.querySelector("img").style.display = "inline";
      button.querySelector("p").style.display = "inline";
      button.removeChild(searchInput);
    },
    async getRecommendations() {
      const trackIds = this.selectedTracks.map(track => track.id).join(",");

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
.get-recommendations {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
  height: 90vh;
}
.outer-section {
  height: 40%;
  width: 90%;
  border-radius: 15px;
  background-color: #202020;
}

.inner-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 90%;
  margin: 1.5vh auto;
}
.inner-section p {
  color: #FFF;
  font-size: x-large;
}
.add-songs-button {
  width: 90%;
  height: 5vh;
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: #202020;
  border: none;
}
.add-songs-button img {
  height: 4vh;
  padding-right: 4%;
}
.add-songs-button p {
  font-size: medium;
}
.get-recommendations-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #0D0D0D;
  color: white;
  text-decoration: none;
  width: 300px;
  height: 10%;
  border-radius: 15px;
  font-weight: bold;
}

.get-recommendations-button img {
  height: 3vh;
  padding-right: 20px;
}

.get-recommendations-button:hover {
  background-color: #171717;
}
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
.dropdown img {
  height: 4vh;
}
</style>