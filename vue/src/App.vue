<template>
  <div>
    <head id="title">
      <link rel="icon" href="@/assets/favicon.png" type="image/png">
    </head>
    <body>
      <nav>
        <a href="/">
          <img src="@/assets/favicon.png" alt="Logo">
          <h1>Spotify Playground</h1>
        </a>
      </nav>
      <main>
        <router-view></router-view>
      </main>
    </body>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Helvetica, Arial, sans-serif;
  background-color: #333;
  color: #f0f0f0;
}

a {
  color: white;
}

nav {
  background-color: #333;
  color: white;
  padding: 0;
  height: 10vh;
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: left;
  border-bottom: 0.5px solid white;
}

nav a {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
  padding: 0 1.5vw;
  height: inherit;
}

nav img {
  max-height: 8vh;
}

nav a:first-child {
  margin-right: auto;
}

nav a:hover {
  background-color: #1c1c1c;
}

main {
  padding: 3vw;
}
</style>





