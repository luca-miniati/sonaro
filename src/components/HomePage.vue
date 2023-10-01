<template>
  <div class="homepage">
    <div class="typewriter-box">
      <h2>Music recommendations,<br>fully <span ref="text"></span></h2>
    </div>
    <div class="login-button">
      <img src="@/assets/spotify.png">
      <a @click=getUserAuthorization>Log In with Spotify</a>
    </div>
  </div>
</template>

<script>
import { v4 } from 'uuid';

export default {
  name: 'HomePage',
  data() {
    return {
      words: ['customized.', 'tailored.', 'personalized.', 'curated.'],
      wordIndex: 0,
      charIndex: 0,
    }
  },
  mounted() {
    this.typeText();
  },
  methods: {
    async getUserAuthorization() {
      const client_id = process.env.VUE_APP_CLIENT_ID;
      const redirect_uri = encodeURIComponent('http://localhost:8000/callback');
      const state = v4();
      const scope = 'user-read-private user-read-recently-played playlist-read-private playlist-read-collaborative user-top-read playlist-modify-public';
      const authorizationUrl = `https://accounts.spotify.com/authorize?` +
        `response_type=code` +
        `&client_id=${client_id}` +
        `&redirect_uri=${redirect_uri}` +
        `&state=${state}` +
        `&scope=${scope}`;

      window.location.href = authorizationUrl;
    },
    typeText() {
      const word = this.words[this.wordIndex];
      // word in progress
      if (this.charIndex < (word.length * 2)) {
        // word adding
        if (this.charIndex < (word.length)) {
          this.$refs.text.innerText += word.charAt(this.charIndex);
          this.charIndex++;
          if (this.charIndex == word.length) {
            setTimeout(this.typeText, 500) 
          } else {
            setTimeout(this.typeText, 100) 
          }
        // word subtracting
        } else {
          this.$refs.text.innerText = this.$refs.text.innerText.slice(0, -1);
          this.charIndex++;
          setTimeout(this.typeText, 100)
        }
      // word completed
      } else {
        this.charIndex = 0;
        this.wordIndex++;
        this.$refs.text.innerText = "";
        if (this.wordIndex >= this.words.length) {
          this.wordIndex = 0;
        }
        setTimeout(this.typeText, 100);
      }
    }
  }
};
</script>

<style scoped>
.homepage {
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 70vh;
}

.login-button {
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

.login-button img {
  height: 3vh;
  padding-right: 20px;
}

.login-button:hover {
  background-color: #171717;
}

.typewriter-box {
  width: 70%;
  text-align: center;
  margin-bottom: 30px;
}

.typewriter-box span {
  color: #CCA4FF;
}
</style>




