<template>
  <div class="findsongs">
    <form @submit.prevent="onSubmit" class="search-box">
      <input ref="searchInput" type="text" placeholder="Search..."> 
    </form>
  </div>
</template>
  
<script>
// import { mapGetters } from 'vuex';

export default {
  name: 'FindSongs',
  methods: {
    onSubmit() {
      const searchInput = this.$refs.searchInput;
      console.log(searchInput.value);
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