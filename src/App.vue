<template>
  <div>
    <head id="title">
      <link rel="icon" href="@/assets/logo.png" type="image/png">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">
    </head>
    <body>
      <nav>
        <a href="/">
          <img src="@/assets/logo.png" alt="Logo">
          <h1>Sonaro</h1>
        </a>
        <a>
          <img src="@/assets/menu.png" alt="Menu">
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
  font-family: 'Lato', sans-serif;
}

body {
  background-color: #303030;
}

nav {
  background-color: #202020;
  height: 10vh;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav a {
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-decoration: none;
  height: inherit;
  color: white;
}

nav img {
  max-height: 8vh;
  padding: 0 2vh;
}

nav a:hover {
  background-color: #1c1c1c;
}
</style>





