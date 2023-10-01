<template>
  <div class="find-tracks">
    <div class="outer-section">
      <p class="section-title">Seed Tracks</p>
      <p id="no-tracks-selected">Add at least 1 track</p>
      <div class="inner-section">
        <button class="add-tracks-button" @click="onClick">
          <img src="@/assets/addtracks.png">
          <p>Add Tracks</p>
        </button>
        <ul v-if="searchResults.length > 0" class="dropdown">
          <li v-for="track in searchResults" :key="track.id" @click="selectTrack(track)">
            <div class="track">
              <img :src="track.album.images[0].url">
              <div class="track-info">
                <p class="track-name">{{ track.name }}</p>
                <div class="artist-info">
                  <p class="artist-name">{{ track.artists.map(a => a.name).join(', ') }}</p>
                </div>
              </div>
            </div>
          </li>
        </ul>
        <ul v-if="selectedTracks.length > 0" class="selected-tracks">
          <li v-for="track in selectedTracks" :key="track.id">
            <div class="track">
              <img :src="track.album.images[0].url">
              <div class="track-info">
                <p class="track-name">{{ track.name }}</p>
                <div class="artist-info">
                  <p class="artist-name">{{ track.artists.map(a => a.name).join(', ') }}</p>
                </div>
              </div>
              <a @click="removeTrack(track)" class="remove-track">
                <img src="@/assets/removetrack.png">
              </a>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="outer-section">
      <p class="section-title">Settings</p>
      <div class="inner-section">
        <div class="setting-section" v-for="(value, key) in settings" :key="key">
          <div class="settings-title">
            <div :class="value">
              <label :for="key">{{ key.slice(0, 1).toUpperCase() + key.slice(1) }}</label>
              <input :id="key" :min="settingsLowerBounds[key]" :max="settingsUpperBounds[key]" v-model="settings[key]"
                @input="onInputChange(key)" />
            </div>
            <a class="settings-info" @click="toggleSettingsInfo(key)">
              <img src="@/assets/settingsinfo.png">
            </a>
          </div>
          <p class="settings-info-text" :id="key + '-info-text'">{{ settingsInfo[key] }}<br>Range: {{ settingsLowerBounds[key] }}-{{
            settingsUpperBounds[key] }}</p>
          <p :id="key + '-outside-range'">Enter a value between {{ settingsLowerBounds[key] }} and {{
            settingsUpperBounds[key] }}</p>
        </div>
      </div>
    </div>

    <div class="get-recommendations-button">
      <img src="@/assets/getrecommendations.png">
      <a @click=getRecommendations>Get Recommendations</a>
    </div>
  </div>
</template>
  
<script>
import '@/components/findtracks.css'
import { mapGetters } from 'vuex'
import axios from 'axios'
import { Buffer } from 'buffer'

export default {
  name: "FindTracks",
  props: ['loading'],
  data() {
    return {
      searching: false,
      searchResults: [],
      selectedTracks: [],
      recommendedTracks: [],
      settings: {
        'limit': 50,
        'energy': 50,
        'popularity': 50,
        'valence': 50,
        'danceability': 50,
        'instrumentalness': 50,
        'acousticness': 50,
        'tempo': 100,
        'liveness': 50,
        'loudness': 50,
        'speechiness': 50,
      },
      // lowest acceptable number for each setting
      settingsLowerBounds: {
        'limit': 1,
        'energy': 0,
        'popularity': 0,
        'valence': 0,
        'danceability': 0,
        'instrumentalness': 0,
        'acousticness': 0,
        'tempo': 1,
        'liveness': 0,
        'loudness': 0,
        'speechiness': 0,
      },
      // highest acceptable number for each setting
      settingsUpperBounds: {
        'limit': 100,
        'energy': 100,
        'popularity': 100,
        'valence': 100,
        'danceability': 100,
        'instrumentalness': 100,
        'acousticness': 100,
        'tempo': 300,
        'liveness': 100,
        'loudness': 100,
        'speechiness': 100,
      },
      settingsInfo: {
        'limit': "Number of songs",
        'energy': "A measure of the perceptual intensity of a track. Energetic tracks tend to feel fast, loud, and vibrant, while less energetic ones may be quieter and more subdued.",
        'popularity': "A measure of a track's popularity, with 0 representing an underground status and 100 signifying mainstream recognition.",
        'valence': "A measure of the musical positivity conveyed by a track. High valence values denote a more positive mood, including happiness, cheerfulness, or euphoria, while low valence values suggest a more negative mood, such as sadness, depression, or anger.",
        'danceability': "A measure of a track's suitability for dancing based on various musical elements, including tempo, rhythm stability, beat strength, and overall regularity.",
        'instrumentalness': "A measure of the likelihood of a song being instrumental (without vocals)",
        'acousticness': "A higher value indicates a more acoustic (non-electronic) sound, while a lower value suggests a stronger presence of electronic elements.",
        'tempo': "A measure the overall speed of a track in beats per minute (BPM)",
        'liveness': "A measure of the probability of a live performance being present in a recording.",
        'loudness': "A measure of the overall volume of a track",
        'speechiness': "A measure of the presence of spoken words in a track.",
      }
    };
  },
  methods: {
    ...mapGetters(["getAccessToken", "getRefreshToken", "getTokenExpiration"]),
    onClick() {
      if (!this.searching) {
        let searchInput = this.searchInput();
        const button = document.querySelector(".add-tracks-button");

        button.querySelector("img").style.display = "none";
        button.querySelector("p").style.display = "none";
        button.appendChild(searchInput);
        searchInput.focus();
        this.searching = true;
      }
    },
    async onSearchInputChange(query) {
      if (query.length === 0) {
        this.searchResults = [];
        return;
      }

      const currentTime = new Date().getTime();
      if (currentTime >= this.getTokenExpiration()) {
        const clientId = process.env.VUE_APP_CLIENT_ID;
        const clientSecret = process.env.VUE_APP_CLIENT_SECRET;
        const refreshOptions = {
          url: 'https://accounts.spotify.com/api/token',
          headers: {
            'Authorization': `Basic ${(Buffer.from(`${clientId}:${clientSecret}`).toString('base64'))}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          params: {
            grant_type: 'refresh_token',
            refresh_token: this.getRefreshToken()
          }
        };

        await axios.post(refreshOptions.url, null, {
          params: refreshOptions.params,
          headers: refreshOptions.headers
        })
          .then(response => {
            this.$store.commit("SET_ACCESS_TOKEN", response.data.access_token)

            const expiration = new Date().getTime() + response.data.expires_in / 1000
            this.$store.commit("SET_TOKEN_EXPIRATION", expiration)
            this.$store.commit("SET_REFRESH_TOKEN", response.data.refresh_token)
          })
      }

      const url = `https://api.spotify.com/v1/search?` +
        `q=${query}` +
        `&type=track` +
        `&limit=5`
      const headers = {
        Authorization: `Bearer ${this.getAccessToken()}`,
      }

      const response = await fetch(url, {
        method: "GET",
        headers: headers,
      })

      if (response.status === 200) {
        const data = await response.json()
        if (data.tracks && data.tracks.items) {
          this.searchResults = data.tracks.items
        } else {
          this.searchResults = []
        }
      } else {
        this.searchResults = []
        console.log("access token: " + this.getAccessToken())
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
        this.onSearchInputChange(event.target.value);
      });

      return elem;
    },
    selectTrack(track) {
      document.querySelector('#no-tracks-selected').style.display = "none"

      this.selectedTracks.push(track)
      this.searchResults = []

      const searchInput = document.querySelector(".search-input")
      searchInput.value = ""

      this.searching = false

      const button = document.querySelector(".add-tracks-button")
      button.querySelector("img").style.display = "inline"
      button.querySelector("p").style.display = "inline"
      button.removeChild(searchInput)
    },
    removeTrack(track) {
      this.selectedTracks.splice(this.selectedTracks.indexOf(track), 1);
    },
    onInputChange(id) {
      if (this.settings[id] < this.settingsLowerBounds[id]
        || this.settings[id] > this.settingsUpperBounds[id]
        || !this.settings[id]) {
        document.querySelector('#' + id + '-outside-range').style.display = 'block'
      } else {
        document.querySelector('#' + id + '-outside-range').style.display = 'none'
      }
    },
    toggleSettingsInfo(id) {
      if (document.querySelector('#' + id + '-info-text').style.display == 'inline-block') {
        document.querySelector('#' + id + '-info-text').style.display = 'none'
      } else {
        document.querySelector('#' + id + '-info-text').style.display = 'inline-block'
      }
    },
    async getRecommendations() {
      if (this.selectedTracks.length == 0) {
        document.querySelector('#no-tracks-selected').style.display = 'block'
        return
      }

      const trackIds = this.selectedTracks.map(track => track.id).join(",");

      let url = `https://api.spotify.com/v1/recommendations?`
        + `seed_tracks=${trackIds}`
        + `&limit=${this.settings['limit']}`
        + `&energy=${this.settings['energy'] / 100}`
        + `&popularity=${this.settings['popularity']}`
        + `&valence=${this.settings['valence'] / 100}`
        + `&danceability=${this.settings['danceability'] / 100}`
        + `&instrumentalness=${this.settings['instrumentalness'] / 100}`
        + `&acousticness=${this.settings['acousticness'] / 100}`
        + `&tempo=${this.settings['tempo']}`
        + `&liveness=${this.settings['liveness'] / 100}`
        + `&loudness=${(this.settings['loudness'] * 0.6) - 60}`
        + `&speechiness=${this.settings['speechiness'] / 100}`;

      const headers = {
        Authorization: `Bearer ${this.getAccessToken()}`,
      }

      const response = await fetch(url, {
        method: "GET",
        headers: headers,
      })

      const data = await response.json()
      this.recommendedTracks = data.tracks

      this.$router.push({ name: 'recommendedtracks', params: { tracks: JSON.stringify(this.recommendedTracks) }})
    },
  }
}
</script>