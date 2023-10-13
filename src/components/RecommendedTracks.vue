<template>
  <div class="recommended-tracks">
    <div class="recommendation-section">
      <p class="section-title">Recommended Tracks</p>
      <div class="track-section">
        <ul class="tracks">
          <li v-for="track in recommendedTracks" :key="track.id">
            <div class="track">
              <img :src="track.album.images[0].url">
              <div class="track-info">
                <p class="track-name">{{ track.name }}</p>
                <div class="artist-info">
                  <p class="artist-name">{{ track.artists.map(a => a.name).join(', ') }}</p>
                </div>
              </div>
              <div class="link-remove-section">
                <a @click="openLink(track)" class="link-track">
                  <img src="@/assets/spotifylink.png">
                </a>
                <a @click="removeTrack(track)" class="remove-track">
                  <img src="@/assets/removetrack.png">
                </a>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="export-button" @click=exportTracks>
      <img src="@/assets/spotify.png">
      <p>Export to Spotify</p>
    </div>
  </div>
</template>

<script>
import '@/components/globals.css'
import axios from 'axios'
import { mapGetters } from 'vuex';


export default {
  name: "RecommendedTracks",
  props: ['tracks'],
  data() {
    return {
      recommendedTracks: []
    }
  },
  created() {
    this.recommendedTracks = [...JSON.parse(this.tracks)]
  },
  methods: {
    ...mapGetters(['getAccessToken']),
    openLink(track) {
      window.open(track.external_urls['spotify'], '_blank')
    },
    removeTrack(track) {
      this.recommendedTracks.splice(this.recommendedTracks.indexOf(track), 1);
    },
    async exportTracks() {
      // Fetch user profile
      const profileUrl = 'https://api.spotify.com/v1/me';
      const profileHeaders = {
        'Authorization': `Bearer ${this.getAccessToken()}`,
        'Content-Type': 'application/json',
      };
      const profileResponse = await axios.get(profileUrl, {
        headers: profileHeaders,
      });
      const userId = profileResponse.data.id;

      // Create playlist
      const playlistUrl = `https://api.spotify.com/v1/users/${userId}/playlists`;
      const playlistHeaders = {
        'Authorization': `Bearer ${this.getAccessToken()}`,
        'Content-Type': 'application/json',
      };
      const playlistData = {
        'name': 'Recommendation Playlist',
        'description': 'by Sonaro',
      };
      const playlistResponse = await axios.post(playlistUrl, playlistData, {
        headers: playlistHeaders,
      });
      const playlistId = playlistResponse.data.id;

      // Update playlist tracks
      const updatePlaylistUrl = `https://api.spotify.com/v1/playlists/${playlistId}/tracks`;
      const uris = this.recommendedTracks.map((track) => track.uri);
      const updatePlaylistData = {
        'uris': uris,
        'position': 0,
      };
      await axios.post(updatePlaylistUrl, updatePlaylistData, {
        headers: {
          'Authorization': `Bearer ${this.getAccessToken()}`,
          'Content-Type': 'application/json',
        },
      });
    },
  }
}
</script>
