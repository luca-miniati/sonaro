<template>
  <div class="findsongs">
    <form @submit.prevent="onSubmit" class="search-box">
      <input ref="searchInput" type="text" placeholder="Search..."> 
    </form>
  </div>
  <!-- <div v-if="searchResults.length > 0" class="search-results">
    <ul>
      <li v-for="(result, index) in searchResults.slice(0, 10)" :key="index">
        <button @click="addToGlobalList(result.id)">{{ result.name }}</button>
      </li>
    </ul>
  </div> -->
</template>
  
<script>
import { mapGetters } from 'vuex';

export default {
  name: 'FindSongs',
  methods: {
    ...mapGetters(['getAccessToken']),
    async onSubmit() {
      const query = this.$refs.searchInput.value;
      const url = `https://api.spotify.com/v1/search` +
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
      console.log(await response.json());
    },
  }
};
</script>

<style scoped>
.findsongs {
  height: 70vh;
  width: 50vw;
}

.search-box input[type="text"] {
  width: 40%;
  border: 1px solid #dbdbdb;
  padding: 1vh 1vh;
  border-radius: 4px;
  font-size: large;
}
</style>